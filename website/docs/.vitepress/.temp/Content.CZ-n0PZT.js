import { usePreferredDark, useDark } from "@vueuse/core";
import { shallowRef, inject, computed, ref, watch, onUnmounted, reactive, markRaw, readonly, nextTick, defineComponent, h } from "vue";
function deserializeFunctions(r) {
  return Array.isArray(r) ? r.map(deserializeFunctions) : typeof r == "object" && r !== null ? Object.keys(r).reduce((t, n) => (t[n] = deserializeFunctions(r[n]), t), {}) : typeof r == "string" && r.startsWith("_vp-fn_") ? new Function(`return ${r.slice(7)}`)() : r;
}
const siteData = deserializeFunctions(JSON.parse('{"lang":"en-SG","dir":"ltr","title":"FOD ARGUS","description":"FOD ARGUS - Autonomous Runway Inspection UAV. NUS CDE4301.","base":"/CDE4301_runway_drone/","head":[],"router":{"prefetchLinks":true},"appearance":"dark","themeConfig":{"siteTitle":false,"nav":[{"text":"Overview","link":"/"},{"text":"Meet the Team","link":"/team"},{"text":"Research","activeMatch":"/research/","items":[{"text":"Primary Research","link":"/research/primary"},{"text":"Secondary Research","link":"/research/secondary"}]},{"text":"Notes","link":"/notes"},{"text":"Drone Specification","link":"/engineering/drone-specification"},{"component":"SubsystemNav"},{"text":"Timeline","link":"/timeline"},{"text":"References","link":"/references"},{"text":"Report","link":"/report/","activeMatch":"/(report/|scopes)"}],"sidebar":{"/report/":[{"text":"PROJECT REPORT","items":[{"text":"Report overview","link":"/report/"},{"text":"Project scope","link":"/scopes"},{"text":"System architecture","link":"/report/system-architecture"}]},{"text":"SUBSYSTEM REPORTS","items":[{"text":"Mechanical Design","link":"/subsystems/mechanical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/mechanical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/mechanical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/mechanical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/mechanical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/mechanical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/mechanical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/mechanical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/mechanical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/mechanical-design/semester-2-development-plan"}]},{"text":"Electrical Design","link":"/subsystems/electrical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/electrical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/electrical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/electrical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/electrical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/electrical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/electrical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/electrical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/electrical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/electrical-design/semester-2-development-plan"}]},{"text":"Navigation & Obstacle Avoidance","link":"/subsystems/navigation-obstacle-avoidance","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/navigation-obstacle-avoidance/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/navigation-obstacle-avoidance/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/navigation-obstacle-avoidance/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/navigation-obstacle-avoidance/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/navigation-obstacle-avoidance/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/navigation-obstacle-avoidance/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/navigation-obstacle-avoidance/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/navigation-obstacle-avoidance/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/navigation-obstacle-avoidance/semester-2-development-plan"}]},{"text":"Computer Vision Based Inspection and Safety System","link":"/subsystems/computer-vision","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/computer-vision/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/computer-vision/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/computer-vision/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/computer-vision/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/computer-vision/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/computer-vision/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/computer-vision/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/computer-vision/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/computer-vision/semester-2-development-plan"}]},{"text":"Communication System","link":"/subsystems/communication-system","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/communication-system/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/communication-system/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/communication-system/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/communication-system/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/communication-system/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/communication-system/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/communication-system/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/communication-system/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/communication-system/semester-2-development-plan"}]}]},{"text":"DEVELOPMENT & SOURCES","items":[{"text":"Timeline","link":"/timeline"},{"text":"Future works","link":"/report/future-works"},{"text":"References","link":"/references"}]}],"/subsystems/":[{"text":"PROJECT REPORT","items":[{"text":"Report overview","link":"/report/"},{"text":"Project scope","link":"/scopes"},{"text":"System architecture","link":"/report/system-architecture"}]},{"text":"SUBSYSTEM REPORTS","items":[{"text":"Mechanical Design","link":"/subsystems/mechanical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/mechanical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/mechanical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/mechanical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/mechanical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/mechanical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/mechanical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/mechanical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/mechanical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/mechanical-design/semester-2-development-plan"}]},{"text":"Electrical Design","link":"/subsystems/electrical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/electrical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/electrical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/electrical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/electrical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/electrical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/electrical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/electrical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/electrical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/electrical-design/semester-2-development-plan"}]},{"text":"Navigation & Obstacle Avoidance","link":"/subsystems/navigation-obstacle-avoidance","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/navigation-obstacle-avoidance/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/navigation-obstacle-avoidance/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/navigation-obstacle-avoidance/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/navigation-obstacle-avoidance/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/navigation-obstacle-avoidance/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/navigation-obstacle-avoidance/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/navigation-obstacle-avoidance/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/navigation-obstacle-avoidance/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/navigation-obstacle-avoidance/semester-2-development-plan"}]},{"text":"Computer Vision Based Inspection and Safety System","link":"/subsystems/computer-vision","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/computer-vision/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/computer-vision/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/computer-vision/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/computer-vision/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/computer-vision/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/computer-vision/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/computer-vision/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/computer-vision/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/computer-vision/semester-2-development-plan"}]},{"text":"Communication System","link":"/subsystems/communication-system","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/communication-system/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/communication-system/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/communication-system/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/communication-system/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/communication-system/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/communication-system/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/communication-system/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/communication-system/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/communication-system/semester-2-development-plan"}]}]},{"text":"DEVELOPMENT & SOURCES","items":[{"text":"Timeline","link":"/timeline"},{"text":"Future works","link":"/report/future-works"},{"text":"References","link":"/references"}]}],"/scopes":[{"text":"PROJECT REPORT","items":[{"text":"Report overview","link":"/report/"},{"text":"Project scope","link":"/scopes"},{"text":"System architecture","link":"/report/system-architecture"}]},{"text":"SUBSYSTEM REPORTS","items":[{"text":"Mechanical Design","link":"/subsystems/mechanical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/mechanical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/mechanical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/mechanical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/mechanical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/mechanical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/mechanical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/mechanical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/mechanical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/mechanical-design/semester-2-development-plan"}]},{"text":"Electrical Design","link":"/subsystems/electrical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/electrical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/electrical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/electrical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/electrical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/electrical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/electrical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/electrical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/electrical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/electrical-design/semester-2-development-plan"}]},{"text":"Navigation & Obstacle Avoidance","link":"/subsystems/navigation-obstacle-avoidance","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/navigation-obstacle-avoidance/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/navigation-obstacle-avoidance/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/navigation-obstacle-avoidance/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/navigation-obstacle-avoidance/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/navigation-obstacle-avoidance/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/navigation-obstacle-avoidance/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/navigation-obstacle-avoidance/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/navigation-obstacle-avoidance/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/navigation-obstacle-avoidance/semester-2-development-plan"}]},{"text":"Computer Vision Based Inspection and Safety System","link":"/subsystems/computer-vision","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/computer-vision/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/computer-vision/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/computer-vision/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/computer-vision/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/computer-vision/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/computer-vision/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/computer-vision/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/computer-vision/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/computer-vision/semester-2-development-plan"}]},{"text":"Communication System","link":"/subsystems/communication-system","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/communication-system/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/communication-system/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/communication-system/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/communication-system/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/communication-system/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/communication-system/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/communication-system/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/communication-system/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/communication-system/semester-2-development-plan"}]}]},{"text":"DEVELOPMENT & SOURCES","items":[{"text":"Timeline","link":"/timeline"},{"text":"Future works","link":"/report/future-works"},{"text":"References","link":"/references"}]}],"/timeline":[{"text":"PROJECT REPORT","items":[{"text":"Report overview","link":"/report/"},{"text":"Project scope","link":"/scopes"},{"text":"System architecture","link":"/report/system-architecture"}]},{"text":"SUBSYSTEM REPORTS","items":[{"text":"Mechanical Design","link":"/subsystems/mechanical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/mechanical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/mechanical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/mechanical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/mechanical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/mechanical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/mechanical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/mechanical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/mechanical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/mechanical-design/semester-2-development-plan"}]},{"text":"Electrical Design","link":"/subsystems/electrical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/electrical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/electrical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/electrical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/electrical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/electrical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/electrical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/electrical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/electrical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/electrical-design/semester-2-development-plan"}]},{"text":"Navigation & Obstacle Avoidance","link":"/subsystems/navigation-obstacle-avoidance","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/navigation-obstacle-avoidance/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/navigation-obstacle-avoidance/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/navigation-obstacle-avoidance/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/navigation-obstacle-avoidance/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/navigation-obstacle-avoidance/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/navigation-obstacle-avoidance/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/navigation-obstacle-avoidance/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/navigation-obstacle-avoidance/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/navigation-obstacle-avoidance/semester-2-development-plan"}]},{"text":"Computer Vision Based Inspection and Safety System","link":"/subsystems/computer-vision","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/computer-vision/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/computer-vision/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/computer-vision/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/computer-vision/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/computer-vision/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/computer-vision/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/computer-vision/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/computer-vision/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/computer-vision/semester-2-development-plan"}]},{"text":"Communication System","link":"/subsystems/communication-system","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/communication-system/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/communication-system/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/communication-system/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/communication-system/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/communication-system/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/communication-system/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/communication-system/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/communication-system/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/communication-system/semester-2-development-plan"}]}]},{"text":"DEVELOPMENT & SOURCES","items":[{"text":"Timeline","link":"/timeline"},{"text":"Future works","link":"/report/future-works"},{"text":"References","link":"/references"}]}],"/references":[{"text":"PROJECT REPORT","items":[{"text":"Report overview","link":"/report/"},{"text":"Project scope","link":"/scopes"},{"text":"System architecture","link":"/report/system-architecture"}]},{"text":"SUBSYSTEM REPORTS","items":[{"text":"Mechanical Design","link":"/subsystems/mechanical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/mechanical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/mechanical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/mechanical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/mechanical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/mechanical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/mechanical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/mechanical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/mechanical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/mechanical-design/semester-2-development-plan"}]},{"text":"Electrical Design","link":"/subsystems/electrical-design","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/electrical-design/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/electrical-design/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/electrical-design/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/electrical-design/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/electrical-design/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/electrical-design/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/electrical-design/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/electrical-design/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/electrical-design/semester-2-development-plan"}]},{"text":"Navigation & Obstacle Avoidance","link":"/subsystems/navigation-obstacle-avoidance","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/navigation-obstacle-avoidance/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/navigation-obstacle-avoidance/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/navigation-obstacle-avoidance/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/navigation-obstacle-avoidance/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/navigation-obstacle-avoidance/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/navigation-obstacle-avoidance/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/navigation-obstacle-avoidance/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/navigation-obstacle-avoidance/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/navigation-obstacle-avoidance/semester-2-development-plan"}]},{"text":"Computer Vision Based Inspection and Safety System","link":"/subsystems/computer-vision","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/computer-vision/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/computer-vision/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/computer-vision/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/computer-vision/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/computer-vision/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/computer-vision/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/computer-vision/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/computer-vision/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/computer-vision/semester-2-development-plan"}]},{"text":"Communication System","link":"/subsystems/communication-system","collapsed":true,"items":[{"text":"1. Executive Summary","link":"/subsystems/communication-system/executive-summary"},{"text":"2. Subsystem Overview","link":"/subsystems/communication-system/subsystem-overview"},{"text":"3. Requirements and Considerations","link":"/subsystems/communication-system/requirements-considerations"},{"text":"4. Design Iterations and Selection","link":"/subsystems/communication-system/design-iterations-selection"},{"text":"5. Detailed Design and Implementation","link":"/subsystems/communication-system/detailed-design-implementation"},{"text":"6. Testing Methodology & Results","link":"/subsystems/communication-system/testing-methodology-results"},{"text":"7. Evaluation & Discussion","link":"/subsystems/communication-system/evaluation-discussion"},{"text":"8. Improvements & Lessons Learned","link":"/subsystems/communication-system/improvements-lessons-learned"},{"text":"9. Semester 2 Development Plan","link":"/subsystems/communication-system/semester-2-development-plan"}]}]},{"text":"DEVELOPMENT & SOURCES","items":[{"text":"Timeline","link":"/timeline"},{"text":"Future works","link":"/report/future-works"},{"text":"References","link":"/references"}]}]},"search":{"provider":"local"},"outline":{"level":[2,3],"label":"On this page"},"footer":{"message":"NUS | College of Design and Engineering","copyright":"FOD ARGUS / CDE4301"}},"locales":{},"scrollOffset":134,"cleanUrls":true}'));
const __vite_import_meta_env__ = {};
const EXTERNAL_URL_RE = /^(?:[a-z]+:|\/\/)/i;
const APPEARANCE_KEY = "vitepress-theme-appearance";
const HASH_RE = /#.*$/;
const HASH_OR_QUERY_RE = /[?#].*$/;
const INDEX_OR_EXT_RE = /(?:(^|\/)index)?\.(?:md|html)$/;
const inBrowser = typeof document !== "undefined";
const notFoundPageData = {
  relativePath: "404.md",
  filePath: "",
  title: "404",
  description: "Not Found",
  headers: [],
  frontmatter: { sidebar: false, layout: "page" },
  lastUpdated: 0,
  isNotFound: true
};
function isActive(currentPath, matchPath, asRegex = false) {
  if (matchPath === void 0) {
    return false;
  }
  currentPath = normalize(`/${currentPath}`);
  if (asRegex) {
    return new RegExp(matchPath).test(currentPath);
  }
  if (normalize(matchPath) !== currentPath) {
    return false;
  }
  const hashMatch = matchPath.match(HASH_RE);
  if (hashMatch) {
    return (inBrowser ? location.hash : "") === hashMatch[0];
  }
  return true;
}
function normalize(path) {
  return decodeURI(path).replace(HASH_OR_QUERY_RE, "").replace(INDEX_OR_EXT_RE, "$1");
}
function isExternal(path) {
  return EXTERNAL_URL_RE.test(path);
}
function getLocaleForPath(siteData2, relativePath) {
  return Object.keys((siteData2 == null ? void 0 : siteData2.locales) || {}).find((key) => key !== "root" && !isExternal(key) && isActive(relativePath, `/${key}/`, true)) || "root";
}
function resolveSiteDataByRoute(siteData2, relativePath) {
  var _a, _b, _c, _d, _e, _f, _g;
  const localeIndex = getLocaleForPath(siteData2, relativePath);
  return Object.assign({}, siteData2, {
    localeIndex,
    lang: ((_a = siteData2.locales[localeIndex]) == null ? void 0 : _a.lang) ?? siteData2.lang,
    dir: ((_b = siteData2.locales[localeIndex]) == null ? void 0 : _b.dir) ?? siteData2.dir,
    title: ((_c = siteData2.locales[localeIndex]) == null ? void 0 : _c.title) ?? siteData2.title,
    titleTemplate: ((_d = siteData2.locales[localeIndex]) == null ? void 0 : _d.titleTemplate) ?? siteData2.titleTemplate,
    description: ((_e = siteData2.locales[localeIndex]) == null ? void 0 : _e.description) ?? siteData2.description,
    head: mergeHead(siteData2.head, ((_f = siteData2.locales[localeIndex]) == null ? void 0 : _f.head) ?? []),
    themeConfig: {
      ...siteData2.themeConfig,
      ...(_g = siteData2.locales[localeIndex]) == null ? void 0 : _g.themeConfig
    }
  });
}
function createTitle(siteData2, pageData) {
  const title = pageData.title || siteData2.title;
  const template = pageData.titleTemplate ?? siteData2.titleTemplate;
  if (typeof template === "string" && template.includes(":title")) {
    return template.replace(/:title/g, title);
  }
  const templateString = createTitleTemplate(siteData2.title, template);
  if (title === templateString.slice(3)) {
    return title;
  }
  return `${title}${templateString}`;
}
function createTitleTemplate(siteTitle, template) {
  if (template === false) {
    return "";
  }
  if (template === true || template === void 0) {
    return ` | ${siteTitle}`;
  }
  if (siteTitle === template) {
    return "";
  }
  return ` | ${template}`;
}
function hasTag(head, tag) {
  const [tagType, tagAttrs] = tag;
  if (tagType !== "meta")
    return false;
  const keyAttr = Object.entries(tagAttrs)[0];
  if (keyAttr == null)
    return false;
  return head.some(([type, attrs]) => type === tagType && attrs[keyAttr[0]] === keyAttr[1]);
}
function mergeHead(prev, curr) {
  return [...prev.filter((tagAttrs) => !hasTag(curr, tagAttrs)), ...curr];
}
const INVALID_CHAR_REGEX = /[\u0000-\u001F"#$&*+,:;<=>?[\]^`{|}\u007F]/g;
const DRIVE_LETTER_REGEX = /^[a-z]:/i;
function sanitizeFileName(name) {
  const match = DRIVE_LETTER_REGEX.exec(name);
  const driveLetter = match ? match[0] : "";
  return driveLetter + name.slice(driveLetter.length).replace(INVALID_CHAR_REGEX, "_").replace(/(^|\/)_+(?=[^/]*$)/, "$1");
}
const KNOWN_EXTENSIONS = /* @__PURE__ */ new Set();
function treatAsHtml(filename) {
  var _a;
  if (KNOWN_EXTENSIONS.size === 0) {
    const extraExts = typeof process === "object" && ((_a = process.env) == null ? void 0 : _a.VITE_EXTRA_EXTENSIONS) || (__vite_import_meta_env__ == null ? void 0 : __vite_import_meta_env__.VITE_EXTRA_EXTENSIONS) || "";
    ("3g2,3gp,aac,ai,apng,au,avif,bin,bmp,cer,class,conf,crl,css,csv,dll,doc,eps,epub,exe,gif,gz,ics,ief,jar,jpe,jpeg,jpg,js,json,jsonld,m4a,man,mid,midi,mjs,mov,mp2,mp3,mp4,mpe,mpeg,mpg,mpp,oga,ogg,ogv,ogx,opus,otf,p10,p7c,p7m,p7s,pdf,png,ps,qt,roff,rtf,rtx,ser,svg,t,tif,tiff,tr,ts,tsv,ttf,txt,vtt,wav,weba,webm,webp,woff,woff2,xhtml,xml,yaml,yml,zip" + (extraExts && typeof extraExts === "string" ? "," + extraExts : "")).split(",").forEach((ext2) => KNOWN_EXTENSIONS.add(ext2));
  }
  const ext = filename.split(".").pop();
  return ext == null || !KNOWN_EXTENSIONS.has(ext.toLowerCase());
}
function escapeRegExp(str) {
  return str.replace(/[|\\{}()[\]^$+*?.]/g, "\\$&").replace(/-/g, "\\x2d");
}
const dataSymbol = Symbol();
const siteDataRef = shallowRef(siteData);
function initData(route) {
  const site = computed(() => resolveSiteDataByRoute(siteDataRef.value, route.data.relativePath));
  const appearance = site.value.appearance;
  const isDark = appearance === "force-dark" ? ref(true) : appearance === "force-auto" ? usePreferredDark() : appearance ? useDark({
    storageKey: APPEARANCE_KEY,
    initialValue: () => appearance === "dark" ? "dark" : "auto",
    ...typeof appearance === "object" ? appearance : {}
  }) : ref(false);
  const hashRef = ref(inBrowser ? location.hash : "");
  if (inBrowser) {
    window.addEventListener("hashchange", () => {
      hashRef.value = location.hash;
    });
  }
  watch(() => route.data, () => {
    hashRef.value = inBrowser ? location.hash : "";
  });
  return {
    site,
    theme: computed(() => site.value.themeConfig),
    page: computed(() => route.data),
    frontmatter: computed(() => route.data.frontmatter),
    params: computed(() => route.data.params),
    lang: computed(() => site.value.lang),
    dir: computed(() => route.data.frontmatter.dir || site.value.dir),
    localeIndex: computed(() => site.value.localeIndex || "root"),
    title: computed(() => createTitle(site.value, route.data)),
    description: computed(() => route.data.description || site.value.description),
    isDark,
    hash: computed(() => hashRef.value)
  };
}
function useData() {
  const data = inject(dataSymbol);
  if (!data) {
    throw new Error("vitepress data not properly injected in app");
  }
  return data;
}
function joinPath(base, path) {
  return `${base}${path}`.replace(/\/+/g, "/");
}
function withBase(path) {
  return EXTERNAL_URL_RE.test(path) || !path.startsWith("/") ? path : joinPath(siteDataRef.value.base, path);
}
function pathToFile(path) {
  let pagePath = path.replace(/\.html$/, "");
  pagePath = decodeURIComponent(pagePath);
  pagePath = pagePath.replace(/\/$/, "/index");
  {
    if (inBrowser) {
      const base = "/CDE4301_runway_drone/";
      pagePath = sanitizeFileName(pagePath.slice(base.length).replace(/\//g, "_") || "index") + ".md";
      let pageHash = __VP_HASH_MAP__[pagePath.toLowerCase()];
      if (!pageHash) {
        pagePath = pagePath.endsWith("_index.md") ? pagePath.slice(0, -9) + ".md" : pagePath.slice(0, -3) + "_index.md";
        pageHash = __VP_HASH_MAP__[pagePath.toLowerCase()];
      }
      if (!pageHash)
        return null;
      pagePath = `${base}${"assets"}/${pagePath}.${pageHash}.js`;
    } else {
      pagePath = `./${sanitizeFileName(pagePath.slice(1).replace(/\//g, "_"))}.md.js`;
    }
  }
  return pagePath;
}
let contentUpdatedCallbacks = [];
function onContentUpdated(fn) {
  contentUpdatedCallbacks.push(fn);
  onUnmounted(() => {
    contentUpdatedCallbacks = contentUpdatedCallbacks.filter((f) => f !== fn);
  });
}
function getScrollOffset() {
  let scrollOffset = siteDataRef.value.scrollOffset;
  let offset = 0;
  let padding = 24;
  if (typeof scrollOffset === "object" && "padding" in scrollOffset) {
    padding = scrollOffset.padding;
    scrollOffset = scrollOffset.selector;
  }
  if (typeof scrollOffset === "number") {
    offset = scrollOffset;
  } else if (typeof scrollOffset === "string") {
    offset = tryOffsetSelector(scrollOffset, padding);
  } else if (Array.isArray(scrollOffset)) {
    for (const selector of scrollOffset) {
      const res = tryOffsetSelector(selector, padding);
      if (res) {
        offset = res;
        break;
      }
    }
  }
  return offset;
}
function tryOffsetSelector(selector, padding) {
  const el = document.querySelector(selector);
  if (!el)
    return 0;
  const bot = el.getBoundingClientRect().bottom;
  if (bot < 0)
    return 0;
  return bot + padding;
}
const RouterSymbol = Symbol();
const fakeHost = "http://a.com";
const getDefaultRoute = () => ({
  path: "/",
  component: null,
  data: notFoundPageData
});
function createRouter(loadPageModule, fallbackComponent) {
  const route = reactive(getDefaultRoute());
  const router = {
    route,
    go
  };
  async function go(href = inBrowser ? location.href : "/") {
    var _a, _b;
    href = normalizeHref(href);
    if (await ((_a = router.onBeforeRouteChange) == null ? void 0 : _a.call(router, href)) === false)
      return;
    if (inBrowser && href !== normalizeHref(location.href)) {
      history.replaceState({ scrollPosition: window.scrollY }, "");
      history.pushState({}, "", href);
    }
    await loadPage(href);
    await ((_b = router.onAfterRouteChange ?? router.onAfterRouteChanged) == null ? void 0 : _b(href));
  }
  let latestPendingPath = null;
  async function loadPage(href, scrollPosition = 0, isRetry = false) {
    var _a, _b;
    if (await ((_a = router.onBeforePageLoad) == null ? void 0 : _a.call(router, href)) === false)
      return;
    const targetLoc = new URL(href, fakeHost);
    const pendingPath = latestPendingPath = targetLoc.pathname;
    try {
      let page = await loadPageModule(pendingPath);
      if (!page) {
        throw new Error(`Page not found: ${pendingPath}`);
      }
      if (latestPendingPath === pendingPath) {
        latestPendingPath = null;
        const { default: comp, __pageData } = page;
        if (!comp) {
          throw new Error(`Invalid route component: ${comp}`);
        }
        await ((_b = router.onAfterPageLoad) == null ? void 0 : _b.call(router, href));
        route.path = inBrowser ? pendingPath : withBase(pendingPath);
        route.component = markRaw(comp);
        route.data = true ? markRaw(__pageData) : readonly(__pageData);
        if (inBrowser) {
          nextTick(() => {
            let actualPathname = siteDataRef.value.base + __pageData.relativePath.replace(/(?:(^|\/)index)?\.md$/, "$1");
            if (!siteDataRef.value.cleanUrls && !actualPathname.endsWith("/")) {
              actualPathname += ".html";
            }
            if (actualPathname !== targetLoc.pathname) {
              targetLoc.pathname = actualPathname;
              href = actualPathname + targetLoc.search + targetLoc.hash;
              history.replaceState({}, "", href);
            }
            if (targetLoc.hash && !scrollPosition) {
              let target = null;
              try {
                target = document.getElementById(decodeURIComponent(targetLoc.hash).slice(1));
              } catch (e) {
                console.warn(e);
              }
              if (target) {
                scrollTo(target, targetLoc.hash);
                return;
              }
            }
            window.scrollTo(0, scrollPosition);
          });
        }
      }
    } catch (err) {
      if (!/fetch|Page not found/.test(err.message) && !/^\/404(\.html|\/)?$/.test(href)) {
        console.error(err);
      }
      if (!isRetry) {
        try {
          const res = await fetch(siteDataRef.value.base + "hashmap.json");
          window.__VP_HASH_MAP__ = await res.json();
          await loadPage(href, scrollPosition, true);
          return;
        } catch (e) {
        }
      }
      if (latestPendingPath === pendingPath) {
        latestPendingPath = null;
        route.path = inBrowser ? pendingPath : withBase(pendingPath);
        route.component = fallbackComponent ? markRaw(fallbackComponent) : null;
        const relativePath = inBrowser ? pendingPath.replace(/(^|\/)$/, "$1index").replace(/(\.html)?$/, ".md").replace(/^\//, "") : "404.md";
        route.data = { ...notFoundPageData, relativePath };
      }
    }
  }
  if (inBrowser) {
    if (history.state === null) {
      history.replaceState({}, "");
    }
    window.addEventListener("click", (e) => {
      if (e.defaultPrevented || !(e.target instanceof Element) || e.target.closest("button") || // temporary fix for docsearch action buttons
      e.button !== 0 || e.ctrlKey || e.shiftKey || e.altKey || e.metaKey)
        return;
      const link = e.target.closest("a");
      if (!link || link.closest(".vp-raw") || link.hasAttribute("download") || link.hasAttribute("target"))
        return;
      const linkHref = link.getAttribute("href") ?? (link instanceof SVGAElement ? link.getAttribute("xlink:href") : null);
      if (linkHref == null)
        return;
      const { href, origin, pathname, hash, search } = new URL(linkHref, link.baseURI);
      const currentUrl = new URL(location.href);
      if (origin === currentUrl.origin && treatAsHtml(pathname)) {
        e.preventDefault();
        if (pathname === currentUrl.pathname && search === currentUrl.search) {
          if (hash !== currentUrl.hash) {
            history.pushState({}, "", href);
            window.dispatchEvent(new HashChangeEvent("hashchange", {
              oldURL: currentUrl.href,
              newURL: href
            }));
          }
          if (hash) {
            scrollTo(link, hash, link.classList.contains("header-anchor"));
          } else {
            window.scrollTo(0, 0);
          }
        } else {
          go(href);
        }
      }
    }, { capture: true });
    window.addEventListener("popstate", async (e) => {
      var _a;
      if (e.state === null)
        return;
      const href = normalizeHref(location.href);
      await loadPage(href, e.state && e.state.scrollPosition || 0);
      await ((_a = router.onAfterRouteChange ?? router.onAfterRouteChanged) == null ? void 0 : _a(href));
    });
    window.addEventListener("hashchange", (e) => {
      e.preventDefault();
    });
  }
  return router;
}
function useRouter() {
  const router = inject(RouterSymbol);
  if (!router) {
    throw new Error("useRouter() is called without provider.");
  }
  return router;
}
function useRoute() {
  return useRouter().route;
}
function scrollTo(el, hash, smooth = false) {
  let target = null;
  try {
    target = el.classList.contains("header-anchor") ? el : document.getElementById(decodeURIComponent(hash).slice(1));
  } catch (e) {
    console.warn(e);
  }
  if (target) {
    let scrollToTarget = function() {
      if (!smooth || Math.abs(targetTop - window.scrollY) > window.innerHeight)
        window.scrollTo(0, targetTop);
      else
        window.scrollTo({ left: 0, top: targetTop, behavior: "smooth" });
    };
    const targetPadding = parseInt(window.getComputedStyle(target).paddingTop, 10);
    const targetTop = window.scrollY + target.getBoundingClientRect().top - getScrollOffset() + targetPadding;
    requestAnimationFrame(scrollToTarget);
  }
}
function normalizeHref(href) {
  const url = new URL(href, fakeHost);
  url.pathname = url.pathname.replace(/(^|\/)index(\.html)?$/, "$1");
  if (siteDataRef.value.cleanUrls)
    url.pathname = url.pathname.replace(/\.html$/, "");
  else if (!url.pathname.endsWith("/") && !url.pathname.endsWith(".html"))
    url.pathname += ".html";
  return url.pathname + url.search + url.hash;
}
const runCbs = () => contentUpdatedCallbacks.forEach((fn) => fn());
const Content = defineComponent({
  name: "VitePressContent",
  props: {
    as: { type: [Object, String], default: "div" }
  },
  setup(props) {
    const route = useRoute();
    const { frontmatter, site } = useData();
    watch(frontmatter, runCbs, { deep: true, flush: "post" });
    return () => h(props.as, site.value.contentProps ?? { style: { position: "relative" } }, [
      route.component ? h(route.component, {
        onVnodeMounted: runCbs,
        onVnodeUpdated: runCbs,
        onVnodeUnmounted: runCbs
      }) : "404 Page Not Found"
    ]);
  }
});
export {
  Content as C,
  EXTERNAL_URL_RE as E,
  RouterSymbol as R,
  isActive as a,
  useRoute as b,
  inBrowser as c,
  createTitle as d,
  initData as e,
  dataSymbol as f,
  getScrollOffset as g,
  createRouter as h,
  isExternal as i,
  useRouter as j,
  escapeRegExp as k,
  mergeHead as m,
  onContentUpdated as o,
  pathToFile as p,
  siteDataRef as s,
  treatAsHtml as t,
  useData as u,
  withBase as w
};
