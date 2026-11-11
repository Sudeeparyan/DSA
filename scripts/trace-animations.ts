import { runTracer } from '../src/lib/tracers';
const demos = [
  ['contains-duplicate', [1,2,3,1]],
  ['two-sum', {nums:[2,7,11,15], target:9}],
  ['valid-parentheses', '()[]{}'],
] as const;
for (const [id, input] of demos) {
  const steps = runTracer(id, input);
  console.log(id, 'steps', steps.length, 'result', steps.at(-1)?.state.result);
}
