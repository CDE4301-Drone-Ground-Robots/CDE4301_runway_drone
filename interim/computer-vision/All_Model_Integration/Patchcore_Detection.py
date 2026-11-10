"""Fast, in-memory Anomalib 2.x PatchCore inference (no Engine / disk frames).

IMPORTANT: Uses default PatchCore ImageNet preprocessing at 256 x 256.
If checkpoint used custom preprocessing / backbone, match training configuration.
Validate score calibration on independent normal and anomalous images.
"""
from pathlib import Path
import os
from unittest.mock import patch
import cv2
import numpy as np
import torch
from anomalib.models import Patchcore

class PatchcoreDetector:
    def __init__(self, checkpoint, image_size=(256, 256), score_threshold=0.05,
                 heatmap_percentile=95, min_region_area=80, padding=20, device=None):
        self.checkpoint = Path(checkpoint).resolve()
        if not self.checkpoint.is_file():
            raise FileNotFoundError(self.checkpoint)
        self.device = torch.device(device or ('cuda:0' if torch.cuda.is_available() else 'cpu'))
        self.image_size = image_size
        self.score_threshold = float(score_threshold)
        self.heatmap_percentile = float(heatmap_percentile)
        self.min_region_area = int(min_region_area)
        self.padding = int(padding)
        # Load checkpoint ONCE, including the trained memory bank.
        # Lightning .ckpt requires consistent architecture with training.
        # PyTorch >=2.6 defaults to weights_only=True and rejects Lightning's
        # trusted Anomalib enum/global objects (e.g., anomalib.PrecisionType).
        # ONLY do this for a checkpoint you personally trained or trust:
        # loading a full checkpoint can execute pickled Python code.
        # Scoped to checkpoint loading, NOT a permanent environment change.
        with patch.dict(os.environ, {'TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD': '1'}):
            try:
                self.model = Patchcore.load_from_checkpoint(
                    str(self.checkpoint), map_location=self.device, visualizer=False)
            except TypeError:
                self.model = Patchcore.load_from_checkpoint(
                    str(self.checkpoint), map_location=self.device)
        self.model.to(self.device).eval()
        # The underlying torch model accepts NCHW tensors directly; unlike the
        # Lightning wrapper, it does not invoke the training/visualization engine.
        self.infer_model = self.model.model
        self.infer_model.eval()
        self.mean = torch.tensor([.485, .456, .406], device=self.device).view(1, 3, 1, 1)
        self.std = torch.tensor([.229, .224, .225], device=self.device).view(1, 3, 1, 1)
        if self.device.type == 'cuda':
            torch.backends.cudnn.benchmark = True

    @torch.inference_mode()
    def detect(self, frame):
        h, w = frame.shape[:2]
        # Match default PredictDataset: square resize, RGB, [0,1], ImageNet normalize.
        # Avoid PIL, PNG writes, dataloaders, Engine initialization per frame.
        rgb = cv2.cvtColor(cv2.resize(frame, (self.image_size[1], self.image_size[0]),
                                           interpolation=cv2.INTER_LINEAR), cv2.COLOR_BGR2RGB)
        x = torch.from_numpy(np.ascontiguousarray(rgb)).to(self.device, non_blocking=True)
        x = x.permute(2, 0, 1).unsqueeze(0).float().div_(255.0)
        x = (x - self.mean) / self.std
        out = self.infer_model(x)
        # Anomalib checkpoint's postprocessor (when present) normalizes score/map.
        # Using raw scores without it may make old thresholds meaningless.
        pp = getattr(self.model, 'post_processor', None)
        if pp is not None:
            out = pp(out)
        score = float(torch.as_tensor(out.pred_score).reshape(-1)[0].item())
        raw = out.anomaly_map
        if raw is None:
            raise RuntimeError('PatchCore returned no anomaly_map')
        amap = torch.as_tensor(raw).detach().float().cpu().numpy().squeeze()
        if amap.ndim != 2:
            raise RuntimeError(f'Unexpected anomaly-map shape: {amap.shape}')
        amap = cv2.resize(amap, (w, h), interpolation=cv2.INTER_LINEAR)
        if not np.isfinite(amap).all():
            raise RuntimeError('Non-finite PatchCore anomaly map')
        if score < self.score_threshold or float(np.ptp(amap)) < 1e-8:
            return {'detected': False, 'boxes': [], 'score': score, 'map': amap}
        cutoff = float(np.percentile(amap, self.heatmap_percentile))
        mask = ((amap >= cutoff) & (amap > float(amap.min()))).astype(np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        count, _, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        boxes = []
        for i in range(1, count):
            x, y, bw, bh, area = map(int, stats[i])
            if area >= self.min_region_area:
                boxes.append((max(0, x-self.padding), max(0, y-self.padding),
                              min(w, x+bw+self.padding), min(h, y+bh+self.padding)))
        return {'detected': bool(boxes), 'boxes': boxes, 'score': score, 'map': amap}

    def close(self):
        pass
