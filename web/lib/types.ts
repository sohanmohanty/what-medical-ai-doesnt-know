export type TrustBand = "stable" | "caution" | "fragile";

export interface DatasetMeta {
  id: string;
  label: string;
  shortLabel: string;
  plainSummary: string;
  difficulty: string;
  exampleFeatures: string[];
}

export interface ModelMeta {
  id: string;
  label: string;
  plainSummary: string;
}

export interface MechanismMeta {
  id: string;
  label: string;
  longLabel: string;
  plainSummary: string;
}

export interface MetricSnapshot {
  meanAccuracy: number;
  meanRocAuc: number;
  meanBrier: number;
  meanEce: number;
}

export interface MetricCard {
  value: number;
  cleanValue: number;
  delta: number;
  status: "holding" | "drifting" | "warning";
}

export interface SeverityInfo {
  label: "mild" | "moderate" | "heavy" | "severe";
  actualRate: number;
  summary: string;
}

export interface ScoreBreakdown {
  trust: number;
  ranking: number;
  calibration: number;
  completeness: number;
}

export interface ReliabilityBin {
  left: number;
  right: number;
  midpoint: number;
  count: number;
  meanPred: number | null;
  fracPositive: number | null;
  absGap: number | null;
}

export interface ReliabilityProfile {
  pooledCount: number;
  observedPositiveRate: number;
  meanPredictedRisk: number;
  meanAbsGap: number;
  maxAbsGap: number;
  bins: ReliabilityBin[];
}

export interface ExplorerScenario extends MetricSnapshot {
  id: string;
  dataset: string;
  model: string;
  mechanism: string;
  rate: number;
  nRuns: number;
  trustBand: TrustBand;
  trustScore: number;
  stabilityScore: number;
  scoreBreakdown: ScoreBreakdown;
  severity: SeverityInfo;
  meanAccuracyChange: number;
  meanRocAucChange: number;
  meanBrierChange: number;
  meanEceChange: number;
  meanTrainActualRate: number;
  meanTestActualRate: number;
  metricCards: {
    rocAuc: MetricCard;
    accuracy: MetricCard;
    brier: MetricCard;
    ece: MetricCard;
  };
  baseline: MetricSnapshot;
  reliability: ReliabilityProfile | null;
  baselineReliability: ReliabilityProfile | null;
}

export interface ComparisonSliceModel {
  model: string;
  rank: number;
  trustScore: number;
  trustBand: TrustBand;
  meanRocAuc: number;
  meanBrier: number;
  meanEce: number;
  meanRocAucChange: number;
  meanBrierChange: number;
  meanEceChange: number;
}

export interface ComparisonSlice {
  id: string;
  dataset: string;
  mechanism: string;
  rate: number;
  bestModel: string;
  models: ComparisonSliceModel[];
}

export interface ExplorerArtifact {
  generatedAtUtc: string;
  source: {
    runName: string;
    summaryPath: string;
    predictionsPath: string;
    baselinePredictionsPath: string | null;
    regime: string;
    imputer: string;
    calibrationBins: number;
    reliabilityAggregation: string;
  };
  defaultSelection: {
    dataset: string;
    model: string;
    mechanism: string;
    rate: number;
  };
  datasets: DatasetMeta[];
  models: ModelMeta[];
  mechanisms: MechanismMeta[];
  rates: number[];
  highlights: {
    mostFragileScenario: {
      dataset: string;
      model: string;
      mechanism: string;
      rate: number;
      trustScore: number;
    };
    mostStableScenario: {
      dataset: string;
      model: string;
      mechanism: string;
      rate: number;
      trustScore: number;
    };
    largestCalibrationDrift: {
      dataset: string;
      model: string;
      mechanism: string;
      rate: number;
      meanEceChange: number;
    };
    largestRankingDrop: {
      dataset: string;
      model: string;
      mechanism: string;
      rate: number;
      meanRocAucChange: number;
    };
  };
  comparisonSlices: ComparisonSlice[];
  scenarios: ExplorerScenario[];
}
