/**
 * Public animation API — import from `@/lib/animation` in app code.
 */
export {
  resolveAnimationSteps,
  animationQualityReport,
} from "./resolve";
export {
  type AnimationState,
  type HighlightKind,
  readPrimaryValues,
  readMemoryShelf,
  readHighlights,
  hasMatchHighlight,
} from "./state";
