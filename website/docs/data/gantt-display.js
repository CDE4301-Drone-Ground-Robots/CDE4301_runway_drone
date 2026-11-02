import source from './gantt.json' with { type: 'json' }

// Editorial changes only. The source JSON keeps the original workbook wording
// and all schedule coordinates, so re-extraction cannot undo these corrections.
const corrections = {
  'O34:O36': 'Prototyping and assembly of the structural prototype',
  'U34:W36': 'Working on the final design iteration and incorporating waterproofing',
  'X37:Y40': 'Obtain necessary certifications and registrations for UAV testing',
  'AA48:AD53': 'Perform complete integration of the vision, communication and navigation systems',
  'Y48:Z53': 'Integrate the communication and vision systems',
  'H51:I53': 'Communication research',
  'U51:X53': 'Communication hardware research, finalisation and purchase',
  'U54:X56': 'Choose and integrate the camera gimbal',
  'AE54:AH56': 'Integrate the thermal camera with Pixhawk',
  'M69:N71': 'Survey method optimisation and rationale',
  'P32:P84': 'Interim presentation: critical function prototype',
  'Q32:Q84': 'Documentation due this week'
}
const properNames = {
  uav: 'UAV', fea: 'FEA', cf: 'CF', '3d': '3D', cv: 'CV', yolo: 'YOLO',
  rgb: 'RGB', ros: 'ROS', px4: 'PX4', pixhawk: 'Pixhawk', jetson: 'Jetson',
  gazebo: 'Gazebo', python: 'Python', 'raspberry pi': 'Raspberry Pi'
}
function sentenceCase(text) {
  return text.trim().replace(/\s+/g, ' ').replace(/\s+([,.])/g, '$1')
    .replace(/([.!?])(?=[A-Za-z])/g, '$1 ').toLowerCase()
    .replace(/\b(?:uav|fea|cf|3d|cv|yolo|rgb|ros|px4|pixhawk|jetson|gazebo|python|raspberry pi)\b/g, word => properNames[word])
    .replace(/(^|[.!?]\s+)([a-z])/g, (_, prefix, letter) => prefix + letter.toUpperCase())
}
function formatTask(task, member) {
  return {
    ...task,
    description: sentenceCase(corrections[task.source] ?? task.description),
    category: member.name === 'Charan' && task.category === 'Calculations' ? 'Camera Integration' : task.category
  }
}
export default {
  ...source,
  weeks: source.weeks.map(week => ({
    ...week,
    label: week.label.replace(/SEM/gi, 'Sem').replace(/RECESS WEEK/gi, 'Recess Week')
      .replace(/READING WEEK/gi, 'Reading Week').replace(/EXAM WEEK/gi, 'Examination Week')
      .replace(/VACATION WEEK/gi, 'Vacation Week')
  })),
  members: source.members.map(member => ({
    ...member,
    tasks: member.tasks.map(task => formatTask(task, member)),
    milestones: member.milestones.map(task => formatTask(task, member))
  }))
}
