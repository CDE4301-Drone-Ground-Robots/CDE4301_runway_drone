export const rubricSections = [
  {
    "slug": "a1-objective-scope-context",
    "title": "1. Objective and Requirements",
    "summary": "Problem, intended deliverables, requirements and context."
  },
  {
    "slug": "a2-methodology-concept-development",
    "title": "2. Methodology / Concept Development",
    "summary": "Methods, design choices and alternatives."
  },
  {
    "slug": "a3-prototype-development",
    "title": "3. Fabrication of Specimens/Prototypes",
    "summary": "Prototype designs, implementation and iterations."
  },
  {
    "slug": "a4-testing",
    "title": "4. Testing",
    "summary": "Test setup, demonstrations and available observations."
  },
  {
    "slug": "a5-analysis",
    "title": "5. Analysis",
    "summary": "Results, calculations, comparisons and interpretation."
  },
  {
    "slug": "a6-problems-project-plan",
    "title": "6. Discussion of Problems and Future Project Plan",
    "summary": "Limitations, remaining work and development plan."
  }
]

const subsystemRubricTitles = {
  "mechanical-design": [
    "1. Objective and Requirements",
    "2. Mechanical Design and Concept Development",
    "3. Mechanical Prototype Development",
    "4. Mechanical Testing and Verification",
    "5. Structural and Propulsion Analysis",
    "6. Discussion of Problems and Future Project Plan"
  ],
  "electrical-design": [
    "1. Objective and Requirements",
    "2. Electrical Design and Component Selection",
    "3. Wiring and Hardware Prototype Development",
    "4. Electrical Testing and Verification",
    "5. Power and Battery Analysis",
    "6. Discussion of Problems and Future Project Plan"
  ],
  "navigation-obstacle-avoidance": [
    "1. Objective and Requirements",
    "2. Navigation Methodology and Concept Development",
    "3. Navigation Prototype Implementation",
    "4. Navigation Simulation Testing",
    "5. Navigation Performance Analysis",
    "6. Discussion of Problems and Future Project Plan"
  ],
  "computer-vision": [
    "1. Objective and Requirements",
    "2. Vision Methodology and Architecture Development",
    "3. Vision Model and Pipeline Implementation",
    "4. Vision Model and Integration Testing",
    "5. Vision Performance and Dataset Analysis",
    "6. Discussion of Problems and Future Project Plan"
  ],
  "communication-system": [
    "1. Objective and Requirements",
    "2. Communication Methodology and Architecture Development",
    "3. Communication Prototype Implementation",
    "4. Communication Testing",
    "5. Communication Performance Analysis",
    "6. Discussion of Problems and Future Project Plan"
  ]
}

export function subsystemRubricSections(subsystem: keyof typeof subsystemRubricTitles) {
 return rubricSections.map((section, index) => ({
  ...section,
  title: subsystemRubricTitles[subsystem][index]
 }))
}
