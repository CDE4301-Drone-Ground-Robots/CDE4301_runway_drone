// Ideal steady-altitude sizing only; the result is an average across four motors.
export const GRAVITY = 9.81
export const MOTOR_COUNT = 4
export const DESIGN_TILT_DEGREES = 45

export function calculateTiltThrust(pitchDegrees: number, rollDegrees: number, massKg: number) {
 const radians = Math.PI / 180
 const cosTilt = Math.cos(pitchDegrees * radians) * Math.cos(rollDegrees * radians)
 const tiltDegrees = Math.acos(Math.min(1, Math.max(-1, cosTilt))) / radians
 const weightN = massKg * GRAVITY
 const totalThrustN = weightN / cosTilt
 const motorThrustN = totalThrustN / MOTOR_COUNT
 return {
  tiltDegrees, weightN, totalThrustN, motorThrustN,
  motorThrustKgf: motorThrustN / GRAVITY,
  thrustRatio: 1 / cosTilt,
  exceedsDesign: tiltDegrees > DESIGN_TILT_DEGREES + 1e-9
 }
}
