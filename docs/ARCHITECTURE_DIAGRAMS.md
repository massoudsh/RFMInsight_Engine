# RFMInsight Engine - Architecture Diagrams

## Table of Contents
1. [High-Level System Overview](#1-high-level-system-overview)
2. [Mid-Level Component Architecture](#2-mid-level-component-architecture)
3. [Low-Level Flow Diagrams](#3-low-level-flow-diagrams)
4. [Data Lineage](#4-data-lineage)
5. [Class Structure](#5-class-structure)
6. [Sequence Diagrams](#6-sequence-diagrams)

---

## 1. High-Level System Overview

### 1.1 Complete System Architecture

```mermaid
graph TD
    subgraph "Input Layer"
        CSV[CSV Transaction Data]
        DB[(Database)]
        API_IN[API Input]
    end

    subgraph "Processing Layer"
        LOADER[Data Loader]
        CLEANER[Data Cleaner]
        CALCULATOR[RFM Calculator]
        SEGMENTER[Customer Segmenter]
    end

    subgraph "Analysis Layer"
        SCORING[RFM Scoring]
        CLUSTERING[ML Clustering]
        PREDICTION[Churn Prediction]
        OPTIMIZATION[Budget Optimizer]
    end

    subgraph "Output Layer"
        REPORTS[PDF Reports]
        VIZ[Visualizations]
        EXPORT[Data Export]
        INSIGHTS[Marketing Insights]
    end

    CSV --> LOADER
    DB --> LOADER
    API_IN --> LOADER
    
    LOADER --> CLEANER
    CLEANER --> CALCULATOR
    
    CALCULATOR --> SCORING
    SCORING --> SEGMENTER
    
    SEGMENTER --> CLUSTERING
    SEGMENTER --> PREDICTION
    SEGMENTER --> OPTIMIZATION
    
    CLUSTERING --> REPORTS
    PREDICTION --> REPORTS
    OPTIMIZATION --> INSIGHTS
    
    SEGMENTER --> VIZ
    SEGMENTER --> EXPORT

    classDef input fill:#e1f5fe
    classDef process fill:#fff3e0
    classDef analysis fill:#e8f5e9
    classDef output fill:#fce4ec
    
    class CSV,DB,API_IN input
    class LOADER,CLEANER,CALCULATOR,SEGMENTER process
    class SCORING,CLUSTERING,PREDICTION,OPTIMIZATION analysis
    class REPORTS,VIZ,EXPORT,INSIGHTS output
```

### 1.2 Simplified System Map

```mermaid
graph LR
    DATA[Transaction Data] --> RFM[RFM Calculator]
    RFM --> SEGMENT[Segmentation]
    SEGMENT --> ML[ML Analysis]
    ML --> INSIGHTS[Actionable Insights]
```

---

## 2. Mid-Level Component Architecture

### 2.1 RFM Calculation Pipeline

```mermaid
flowchart TB
    subgraph "Data Ingestion"
        RAW[Raw Transactions]
        VALIDATE[Schema Validation]
        CLEAN[Data Cleaning]
    end

    subgraph "RFM Calculation"
        RECENCY[Calculate Recency]
        FREQUENCY[Calculate Frequency]
        MONETARY[Calculate Monetary]
        AGGREGATE[Aggregate per Customer]
    end

    subgraph "Scoring"
        QUINTILES[Calculate Quintiles]
        R_SCORE[R Score 1-5]
        F_SCORE[F Score 1-5]
        M_SCORE[M Score 1-5]
        RFM_SCORE[Combined RFM Score]
    end

    subgraph "Segmentation"
        RULES[Rule-Based Segments]
        KMEANS[K-Means Clustering]
        FINAL_SEGMENT[Final Segments]
    end

    RAW --> VALIDATE
    VALIDATE --> CLEAN
    
    CLEAN --> RECENCY
    CLEAN --> FREQUENCY
    CLEAN --> MONETARY
    
    RECENCY --> AGGREGATE
    FREQUENCY --> AGGREGATE
    MONETARY --> AGGREGATE
    
    AGGREGATE --> QUINTILES
    QUINTILES --> R_SCORE
    QUINTILES --> F_SCORE
    QUINTILES --> M_SCORE
    
    R_SCORE --> RFM_SCORE
    F_SCORE --> RFM_SCORE
    M_SCORE --> RFM_SCORE
    
    RFM_SCORE --> RULES
    RFM_SCORE --> KMEANS
    RULES --> FINAL_SEGMENT
    KMEANS --> FINAL_SEGMENT
```

### 2.2 Customer Segments

```mermaid
flowchart TB
    subgraph "Champion Customers"
        CHAMP[R=5, F=5, M=5]
        CHAMP_DESC[Bought recently, buy often, spend most]
    end

    subgraph "Loyal Customers"
        LOYAL[R=3-5, F=4-5, M=4-5]
        LOYAL_DESC[Buy regularly, responsive to promotions]
    end

    subgraph "Potential Loyalists"
        POTENTIAL[R=4-5, F=2-4, M=2-4]
        POTENTIAL_DESC[Recent customers with potential]
    end

    subgraph "At Risk"
        ATRISK[R=2-3, F=3-5, M=3-5]
        ATRISK_DESC[Used to purchase frequently, need attention]
    end

    subgraph "Hibernating"
        HIBERNATE[R=1-2, F=1-2, M=1-2]
        HIBERNATE_DESC[Low engagement, may be lost]
    end

    subgraph "Lost"
        LOST[R=1, F=1-2, M=1-5]
        LOST_DESC[Haven't purchased in long time]
    end
```

### 2.3 Analysis Modules

```mermaid
flowchart TB
    subgraph "Core Analysis"
        RFM_CALC[RFM Calculator]
        SEGMENT[Segmentation Engine]
    end

    subgraph "ML Analysis"
        CLUSTER[K-Means Clustering]
        PREDICT[Churn Predictor]
        LTV[CLV Calculator]
    end

    subgraph "Optimization"
        BUDGET[Budget Allocator]
        CAMPAIGN[Campaign Optimizer]
        TIMING[Timing Optimizer]
    end

    subgraph "Reporting"
        PDF_GEN[PDF Generator]
        PLOT[Visualization Engine]
        EXPORT[Data Exporter]
    end

    RFM_CALC --> SEGMENT
    SEGMENT --> CLUSTER
    SEGMENT --> PREDICT
    SEGMENT --> LTV
    
    CLUSTER --> BUDGET
    PREDICT --> CAMPAIGN
    LTV --> BUDGET
    
    BUDGET --> PDF_GEN
    CAMPAIGN --> PDF_GEN
    SEGMENT --> PLOT
    SEGMENT --> EXPORT
```

---

## 3. Low-Level Flow Diagrams

### 3.1 Full Analysis Pipeline

```mermaid
flowchart TD
    START[Start Analysis] --> LOAD[Load Transaction Data]
    LOAD --> VALIDATE{Valid Schema?}
    
    VALIDATE -->|No| ERROR[Raise Validation Error]
    VALIDATE -->|Yes| CLEAN[Clean & Preprocess]
    
    CLEAN --> CALC_R[Calculate Recency per Customer]
    CALC_R --> CALC_F[Calculate Frequency per Customer]
    CALC_F --> CALC_M[Calculate Monetary per Customer]
    
    CALC_M --> SCORE[Apply Quintile Scoring]
    SCORE --> COMBINE[Combine into RFM Score]
    
    COMBINE --> SEG_RULE[Apply Rule-Based Segmentation]
    COMBINE --> SEG_ML[Apply ML Clustering]
    
    SEG_RULE --> MERGE[Merge Segmentation Results]
    SEG_ML --> MERGE
    
    MERGE --> ANALYZE[Generate Analytics]
    ANALYZE --> VIZ[Create Visualizations]
    VIZ --> REPORT[Generate PDF Report]
    REPORT --> EXPORT[Export Results]
    EXPORT --> END[Complete]
```

### 3.2 Churn Prediction Flow

```mermaid
flowchart TD
    INPUT[Customer RFM Data] --> FEATURES[Extract Features]
    
    FEATURES --> RECENCY[Recency Score]
    FEATURES --> TREND[Purchase Trend]
    FEATURES --> AVG_ORDER[Avg Order Value]
    FEATURES --> LAST_GAP[Days Since Last Purchase]
    
    RECENCY --> FEATURE_VEC[Feature Vector]
    TREND --> FEATURE_VEC
    AVG_ORDER --> FEATURE_VEC
    LAST_GAP --> FEATURE_VEC
    
    FEATURE_VEC --> MODEL{Model Type}
    
    MODEL -->|Random Forest| RF[RF Classifier]
    MODEL -->|Gradient Boost| GB[XGBoost]
    MODEL -->|Logistic| LR[Logistic Regression]
    
    RF --> PREDICT[Churn Probability]
    GB --> PREDICT
    LR --> PREDICT
    
    PREDICT --> CLASSIFY{Risk Level}
    CLASSIFY -->|>70%| HIGH[High Risk]
    CLASSIFY -->|30-70%| MEDIUM[Medium Risk]
    CLASSIFY -->|<30%| LOW[Low Risk]
    
    HIGH --> ACTION[Retention Actions]
    MEDIUM --> ACTION
    LOW --> MONITOR[Continue Monitoring]
```

### 3.3 Budget Optimization Flow

```mermaid
flowchart TD
    BUDGET[Total Marketing Budget] --> SEGMENTS[Customer Segments]
    
    SEGMENTS --> CALC_VALUE[Calculate Segment Value]
    SEGMENTS --> CALC_SIZE[Calculate Segment Size]
    SEGMENTS --> CALC_RESPONSE[Estimate Response Rate]
    
    CALC_VALUE --> PRIORITY[Priority Score]
    CALC_SIZE --> PRIORITY
    CALC_RESPONSE --> PRIORITY
    
    PRIORITY --> ALLOCATE[Allocate Budget]
    
    ALLOCATE --> CHAMPS[Champions: 15%]
    ALLOCATE --> LOYAL[Loyal: 20%]
    ALLOCATE --> POTENTIAL[Potential: 25%]
    ALLOCATE --> ATRISK[At Risk: 30%]
    ALLOCATE --> OTHER[Others: 10%]
    
    CHAMPS --> RECOMMEND[Campaign Recommendations]
    LOYAL --> RECOMMEND
    POTENTIAL --> RECOMMEND
    ATRISK --> RECOMMEND
    OTHER --> RECOMMEND
```

---

## 4. Data Lineage

### 4.1 Transaction to Segment Lineage

```mermaid
flowchart TB
    subgraph "Raw Data"
        TX[Transaction Records]
    end

    subgraph "Cleaned Data"
        CUSTOMER_ID[customer_id]
        TX_DATE[transaction_date]
        AMOUNT[amount]
    end

    subgraph "Aggregated Metrics"
        LAST_TX[Last Transaction Date]
        TX_COUNT[Transaction Count]
        TOTAL_SPEND[Total Spend]
    end

    subgraph "RFM Scores"
        R_DAYS[Recency in Days]
        R_SCORE[R Score 1-5]
        F_SCORE[F Score 1-5]
        M_SCORE[M Score 1-5]
    end

    subgraph "Final Output"
        SEGMENT[Customer Segment]
        ACTIONS[Recommended Actions]
        METRICS[Segment Metrics]
    end

    TX --> CUSTOMER_ID
    TX --> TX_DATE
    TX --> AMOUNT
    
    TX_DATE --> LAST_TX
    CUSTOMER_ID --> TX_COUNT
    AMOUNT --> TOTAL_SPEND
    
    LAST_TX --> R_DAYS
    R_DAYS --> R_SCORE
    TX_COUNT --> F_SCORE
    TOTAL_SPEND --> M_SCORE
    
    R_SCORE --> SEGMENT
    F_SCORE --> SEGMENT
    M_SCORE --> SEGMENT
    
    SEGMENT --> ACTIONS
    SEGMENT --> METRICS
```

### 4.2 Report Generation Lineage

```mermaid
flowchart TB
    subgraph "Analysis Results"
        SEGMENTS[Customer Segments]
        METRICS[RFM Metrics]
        PREDICTIONS[Churn Predictions]
    end

    subgraph "Visualization"
        DIST_PLOT[Segment Distribution]
        RFM_HEATMAP[RFM Heatmap]
        TREND_CHART[Trend Charts]
        CHURN_CHART[Churn Risk Chart]
    end

    subgraph "Report Components"
        EXEC_SUMMARY[Executive Summary]
        SEGMENT_DETAIL[Segment Details]
        ACTION_ITEMS[Action Items]
        APPENDIX[Data Appendix]
    end

    subgraph "Output"
        PDF[PDF Report]
        CSV[CSV Export]
        JSON[JSON API Response]
    end

    SEGMENTS --> DIST_PLOT
    SEGMENTS --> SEGMENT_DETAIL
    METRICS --> RFM_HEATMAP
    METRICS --> TREND_CHART
    PREDICTIONS --> CHURN_CHART
    
    DIST_PLOT --> EXEC_SUMMARY
    SEGMENT_DETAIL --> EXEC_SUMMARY
    CHURN_CHART --> ACTION_ITEMS
    
    EXEC_SUMMARY --> PDF
    SEGMENT_DETAIL --> PDF
    ACTION_ITEMS --> PDF
    APPENDIX --> PDF
    
    SEGMENTS --> CSV
    SEGMENTS --> JSON
```

---

## 5. Class Structure

### 5.1 Core Classes

```mermaid
classDiagram
    class RFMEngine {
        +DataFrame data
        +Dict config
        +analyze() RFMResult
        +calculate_rfm() DataFrame
        +segment_customers() DataFrame
        +generate_report() Report
    }

    class DataLoader {
        +String filepath
        +load_csv() DataFrame
        +load_database() DataFrame
        +validate_schema() bool
        +clean_data() DataFrame
    }

    class RFMCalculator {
        +DataFrame transactions
        +Date reference_date
        +calculate_recency() Series
        +calculate_frequency() Series
        +calculate_monetary() Series
        +score_rfm() DataFrame
    }

    class Segmenter {
        +DataFrame rfm_data
        +List segments
        +rule_based_segment() DataFrame
        +kmeans_segment(n_clusters) DataFrame
        +get_segment_profile() Dict
    }

    class ReportGenerator {
        +RFMResult results
        +generate_pdf(filepath)
        +generate_visualizations() List
        +export_csv(filepath)
    }

    RFMEngine --> DataLoader
    RFMEngine --> RFMCalculator
    RFMEngine --> Segmenter
    RFMEngine --> ReportGenerator
    RFMCalculator --> Segmenter
```

### 5.2 Analysis Classes

```mermaid
classDiagram
    class ChurnPredictor {
        +DataFrame customer_data
        +Model model
        +train(X, y)
        +predict(X) Array
        +predict_proba(X) Array
        +feature_importance() Dict
    }

    class CLVCalculator {
        +DataFrame transactions
        +float discount_rate
        +calculate_clv() Series
        +project_revenue(months) float
        +segment_by_clv() DataFrame
    }

    class BudgetOptimizer {
        +float total_budget
        +Dict segment_metrics
        +optimize() Dict
        +recommend_allocation() Dict
        +estimate_roi() float
    }

    class CampaignRecommender {
        +Dict segments
        +recommend_campaigns() List
        +suggest_timing() Dict
        +prioritize_segments() List
    }

    ChurnPredictor --> CLVCalculator
    CLVCalculator --> BudgetOptimizer
    BudgetOptimizer --> CampaignRecommender
```

### 5.3 Data Models

```mermaid
classDiagram
    class Transaction {
        +String customer_id
        +DateTime date
        +float amount
        +String product_id
        +String category
    }

    class Customer {
        +String id
        +float recency
        +int frequency
        +float monetary
        +int r_score
        +int f_score
        +int m_score
        +String segment
    }

    class Segment {
        +String name
        +String description
        +int customer_count
        +float avg_recency
        +float avg_frequency
        +float avg_monetary
        +float total_revenue
        +List actions
    }

    class RFMResult {
        +DataFrame customers
        +List segments
        +Dict metrics
        +List visualizations
        +Dict recommendations
    }

    Transaction --> Customer
    Customer --> Segment
    Segment --> RFMResult
```

---

## 6. Sequence Diagrams

### 6.1 Full Analysis Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant E as RFMEngine
    participant L as DataLoader
    participant C as RFMCalculator
    participant S as Segmenter
    participant R as ReportGenerator

    U->>E: analyze(filepath)
    E->>L: load_csv(filepath)
    L->>L: validate_schema()
    L->>L: clean_data()
    L-->>E: DataFrame

    E->>C: calculate_rfm(data)
    C->>C: calculate_recency()
    C->>C: calculate_frequency()
    C->>C: calculate_monetary()
    C->>C: score_rfm()
    C-->>E: RFM DataFrame

    E->>S: segment_customers(rfm_data)
    S->>S: rule_based_segment()
    S->>S: kmeans_segment()
    S->>S: merge_segments()
    S-->>E: Segmented DataFrame

    E->>R: generate_report(results)
    R->>R: generate_visualizations()
    R->>R: create_pdf()
    R-->>E: Report

    E-->>U: RFMResult
```

### 6.2 Churn Analysis Sequence

```mermaid
sequenceDiagram
    participant E as RFMEngine
    participant P as ChurnPredictor
    participant F as FeatureExtractor
    participant M as Model

    E->>P: predict_churn(customers)
    P->>F: extract_features(customers)
    
    F->>F: recency_features()
    F->>F: frequency_features()
    F->>F: trend_features()
    F-->>P: Feature Matrix
    
    P->>M: predict_proba(features)
    M-->>P: Probabilities
    
    P->>P: classify_risk(probabilities)
    P->>P: generate_actions(risk_levels)
    P-->>E: ChurnResult
```

### 6.3 Report Generation Sequence

```mermaid
sequenceDiagram
    participant E as RFMEngine
    participant R as ReportGenerator
    participant V as Visualizer
    participant P as PDFWriter

    E->>R: generate_report(results)
    
    R->>V: create_segment_chart(segments)
    V-->>R: segment_chart.png
    
    R->>V: create_rfm_heatmap(rfm_data)
    V-->>R: heatmap.png
    
    R->>V: create_trend_charts(metrics)
    V-->>R: trends.png
    
    R->>P: init_document()
    R->>P: add_executive_summary()
    R->>P: add_visualizations(charts)
    R->>P: add_segment_details()
    R->>P: add_recommendations()
    R->>P: save(filepath)
    
    P-->>R: PDF saved
    R-->>E: Report complete
```

---

## 7. Unified System Map

```mermaid
graph TB
    subgraph "RFMInsight Engine"
        subgraph "Input"
            DATA[Transaction Data]
        end

        subgraph "Processing"
            LOAD[Data Loader]
            CALC[RFM Calculator]
            SEG[Segmenter]
        end

        subgraph "Analysis"
            ML[ML Clustering]
            CHURN[Churn Prediction]
            CLV[CLV Calculation]
        end

        subgraph "Optimization"
            BUDGET[Budget Optimizer]
            CAMPAIGN[Campaign Recommender]
        end

        subgraph "Output"
            REPORT[PDF Reports]
            VIZ[Visualizations]
            EXPORT[Data Export]
        end
    end

    DATA --> LOAD
    LOAD --> CALC
    CALC --> SEG
    
    SEG --> ML
    SEG --> CHURN
    SEG --> CLV
    
    ML --> BUDGET
    CHURN --> CAMPAIGN
    CLV --> BUDGET
    
    BUDGET --> REPORT
    CAMPAIGN --> REPORT
    SEG --> VIZ
    SEG --> EXPORT

    classDef input fill:#e1f5fe
    classDef process fill:#c8e6c9
    classDef analysis fill:#fff3e0
    classDef optimize fill:#fce4ec
    classDef output fill:#f3e5f5

    class DATA input
    class LOAD,CALC,SEG process
    class ML,CHURN,CLV analysis
    class BUDGET,CAMPAIGN optimize
    class REPORT,VIZ,EXPORT output
```

---

## Usage

View these diagrams in:
- GitHub/GitLab markdown preview
- VS Code with Mermaid extension
- [Mermaid Live Editor](https://mermaid.live/)
