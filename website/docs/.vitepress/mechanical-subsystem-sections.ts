import { subsystemRubricSections } from './rubric-sections'

export type MechanicalSection = {
 slug: string
 title: string
 sections?: MechanicalSection[]
}

export const mechanicalSubsystemSections: MechanicalSection[] = [
  {
    "slug": "a1-objective-scope-context",
    "title": "A1. Objective, Scope and Context",
    "sections": [
      {
        "slug": "overview-of-mechanical-design-of-the-uav",
        "title": "1.1 Mechanical Design Objectives and Scope"
      },
      {
        "slug": "mechanical-design-requirements-considerations",
        "title": "1.2 Mechanical Design Requirements and Considerations"
      }
    ]
  },
  {
    "slug": "a2-methodology-concept-development",
    "title": "A2. Methodology / Concept Development",
    "sections": [
      {
        "slug": "initial-concept-sketch",
        "title": "2.1 Initial Concept Sketch"
      },
      {
        "slug": "uav-configuration-selection",
        "title": "2.2 UAV Configuration Selection",
        "sections": [
          {
            "slug": "plus-vs-x-vs-h-propeller-configuration",
            "title": "2.2.1 Plus vs X vs H Configuration"
          },
          {
            "slug": "pusher-vs-puller-configuration",
            "title": "2.2.2 Pusher vs Puller Configuration"
          }
        ]
      },
      {
        "slug": "design-iterations",
        "title": "2.3 Mechanical Design Iterations",
        "sections": [
          {
            "slug": "first-iteration",
            "title": "2.3.1 First Design Iteration"
          },
          {
            "slug": "cfrp-sheets-tubes-vs-3d-printed-parts",
            "title": "2.3.2 CFRP Sheets & Tubes vs 3D-Printed Parts"
          },
          {
            "slug": "second-iteration",
            "title": "2.3.3 Second Design Iteration"
          }
        ]
      },
      {
        "slug": "motor-propellers-selection",
        "title": "2.4 Motor and Propeller Selection",
        "sections": [
          {
            "slug": "_5-1-preliminary-mass-estimation-and-component-placement",
            "title": "2.4.1 Preliminary Mass Estimation"
          },
          {
            "slug": "_5-2-preliminary-thrust-calculations",
            "title": "2.4.2 Preliminary Thrust Calculations"
          },
          {
            "slug": "_5-3-setting-conservative-thrust-estimate",
            "title": "2.4.3 Conservative Thrust Estimation"
          },
          {
            "slug": "_5-4-motors-and-propellers-evaluation",
            "title": "2.4.4 Motor and Propeller Evaluation"
          },
          {
            "slug": "_5-5-differential-motor-thrust-calculation",
            "title": "2.4.5 Differential Motor Thrust Calculations"
          }
        ]
      },
      {
        "slug": "propeller-arm-selection",
        "title": "2.5 Propeller Arm Selection",
        "sections": [
          {
            "slug": "bending-stress-calculation",
            "title": "2.5.1 Bending Stress Calculation"
          },
          {
            "slug": "beam-deflection-calculation",
            "title": "2.5.2 Beam Deflection Calculation"
          },
          {
            "slug": "natural-bending-frequency-calculation",
            "title": "2.5.3 Natural Bending Frequency Calculation"
          },
          {
            "slug": "evaluation-of-different-beam-configurations",
            "title": "2.5.4 Evaluation of Different Tube Configurations"
          }
        ]
      },
      {
        "slug": "final-prototype-design",
        "title": "2.6 Third Design Iteration (Final Prototype Design)"
      },
      {
        "slug": "placement-of-key-onboard-components",
        "title": "2.7 Placement of Key Onboard Components",
        "sections": [
          {
            "slug": "central-alignment-of-gnss-antenna-and-rgb-camera",
            "title": "Central Alignment of GNSS Antenna and RGB Camera"
          },
          {
            "slug": "placement-of-the-pixhawk-flight-controller-near-centre-of-gravity",
            "title": "Placement of the Pixhawk Flight Controller near Centre of Gravity"
          },
          {
            "slug": "placement-of-the-360-lidar",
            "title": "Placement of the 360° LiDAR"
          },
          {
            "slug": "45-degree-placement-of-the-thermal-camera",
            "title": "45° Placement of the Thermal Camera"
          },
          {
            "slug": "placement-of-batteries-and-other-electrical-components-in-the-bottom-layer",
            "title": "Placement of Batteries and Other Electrical Components in the Bottom Layer"
          }
        ]
      }
    ]
  },
  {
    "slug": "a3-prototype-development",
    "title": "A3. Fabrication of Specimens/Prototypes",
    "sections": [
      {
        "slug": "structural-prototype",
        "title": "3.1 Structural Prototype"
      },
      {
        "slug": "3d-printed-carbon-fibre-tube-clamps",
        "title": "3.2 3D-Printed Carbon Fibre Tube Clamps"
      },
      {
        "slug": "3d-printed-drone-leg-mounts",
        "title": "3.3 3D-Printed Drone Leg Mounts"
      }
    ]
  },
  {
    "slug": "a4-testing",
    "title": "A4. Testing",
    "sections": [
      {
        "slug": "motor-testing",
        "title": "4.1 Motor Testing",
        "sections": [
          {
            "slug": "individual-motor-testing-mavproxy",
            "title": "4.1.1 Individual Motor Testing Using MAVProxy"
          },
          {
            "slug": "simultaneous-motor-testing-mission-planner",
            "title": "4.1.2 Simultaneous Motor Testing Using Mission Planner"
          }
        ]
      }
    ]
  },
  {
    "slug": "a5-analysis",
    "title": "5. Mechanical Analysis",
    "sections": [
      {
        "slug": "centre-of-gravity-cg-of-uav",
        "title": "5.1 Centre of Gravity (CG) Analysis",
        "sections": [
          {
            "slug": "horizontal-cg-positioning",
            "title": "Horizontal CG Positioning"
          },
          {
            "slug": "vertical-cg-positioning",
            "title": "Vertical CG Positioning"
          }
        ]
      },
      {
        "slug": "tube-clamp-analysis-after-testing",
        "title": "5.2 3D-Printed Carbon Fibre Tube Clamp Analysis After Testing"
      },
      {
        "slug": "drone-leg-mount-analysis-after-testing",
        "title": "5.3 3D-Printed Drone Leg Mount Analysis After Testing"
      }
    ]
  },
  {
    "slug": "a6-problems-project-plan",
    "title": "6. Discussion of Future Works",
    "sections": [
      {
        "slug": "semester-2-development-plan",
        "title": "6.1 Semester 2 Development Plan",
        "sections": [
          {
            "slug": "waterproofing-onboard-electronics",
            "title": "6.1.1 Waterproofing and Protection of Onboard Electronics"
          },
          {
            "slug": "base-plate-structural-validation",
            "title": "6.1.2 Base Plate Finalisation and Structural Validation"
          },
          {
            "slug": "jetson-water-resistant-ventilation",
            "title": "6.1.3 Water-Resistant Ventilation for Jetson Orin NX"
          },
          {
            "slug": "additional-vibration-damping",
            "title": "6.1.4 Additional Vibration-Damping Measures"
          },
          {
            "slug": "uav-flight-testing-calibration",
            "title": "6.1.5 UAV Flight Testing and Calibration"
          }
        ]
      }
    ]
  }
].map((section, index) => ({ ...section, title: subsystemRubricSections('mechanical-design')[index].title }))

type MechanicalSidebarItem = { text: string; link: string; collapsed?: boolean; items?: MechanicalSidebarItem[] }

export function numberedMechanicalSections(sections = mechanicalSubsystemSections): MechanicalSidebarItem[] {
 return sections.map(section => ({
  text: section.title,
  link: '/subsystems/mechanical-design#' + section.slug,
  ...(section.sections?.length ? { collapsed: true, items: numberedMechanicalSections(section.sections) } : {})
 }))
}

export function flattenMechanicalSections(sections = mechanicalSubsystemSections): MechanicalSection[] {
 return sections.flatMap(section => [section, ...flattenMechanicalSections(section.sections ?? [])])
}
