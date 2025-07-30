#!/usr/bin/env python3
"""
Advanced StepChain Workflows

This example demonstrates complex, production-ready workflows including:
- Data pipeline orchestration
- Multi-stage analysis with checkpoints
- Error recovery and partial retries
- Custom tool integration
- Progress monitoring
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from stepchain import decompose, execute, setup_stepchain
from stepchain.core import Executor, Plan, StepResult


# Example 1: Data Pipeline with Checkpoints
def data_pipeline_example():
    """
    Complex data pipeline that processes large datasets with checkpoint recovery.
    """
    print("\n=== Data Pipeline with Checkpoints ===")
    
    # Define pipeline tools
    tools = [
        {
            "type": "mcp",
            "server_label": "data_warehouse",
            "server_url": "postgresql://warehouse.company.com:5432/analytics",
            "allowed_tools": ["query", "export_data", "create_view"],
        },
        {
            "type": "mcp",
            "server_label": "s3_storage",
            "server_url": "s3://data-lake.company.com",
            "allowed_tools": ["upload_file", "list_files", "download_file"],
        },
        "code_interpreter",  # For data transformation
        {
            "type": "function",
            "function": {
                "name": "validate_data",
                "description": "Validate data quality and completeness",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data_path": {"type": "string"},
                        "rules": {"type": "object"}
                    }
                }
            },
            "implementation": lambda data_path, rules: {
                "valid": True, 
                "issues": [],
                "row_count": 150000
            }
        }
    ]
    
    # Complex multi-stage pipeline
    pipeline_task = """
    Execute monthly customer analytics pipeline:
    
    1. Extract customer data from data warehouse (last 30 days)
    2. Extract transaction data from data warehouse (last 30 days)
    3. Join customer and transaction data
    4. Calculate customer lifetime value (CLV)
    5. Segment customers based on CLV and behavior
    6. Generate statistical summaries for each segment
    7. Create visualizations for key metrics
    8. Validate all output data
    9. Upload processed data to S3 data lake
    10. Create summary report
    11. Update data warehouse views for BI tools
    """
    
    # Decompose into executable plan
    plan = decompose(pipeline_task, tools=tools, max_steps=20)
    
    # Execute with checkpoint recovery
    run_id = f"monthly_pipeline_{datetime.now().strftime('%Y%m%d')}"
    
    try:
        # First execution attempt
        results = execute(plan, run_id=run_id)
        print(f"Pipeline completed: {len([r for r in results if r.status == 'completed'])} steps")
        
    except KeyboardInterrupt:
        print("\nPipeline interrupted! State saved automatically.")
        print(f"Resume with: execute(plan, run_id='{run_id}', resume=True)")
        
        # Simulate resume after interruption
        input("\nPress Enter to simulate resume...")
        
        # Resume from exact interruption point
        results = execute(plan, run_id=run_id, resume=True)
        print(f"Pipeline resumed and completed successfully!")


# Example 2: Multi-Model Analysis Workflow
def multi_model_analysis():
    """
    Orchestrate analysis across multiple AI models and data sources.
    """
    print("\n=== Multi-Model Analysis Workflow ===")
    
    # Custom model comparison function
    def compare_predictions(predictions: List[Dict]) -> Dict:
        """Compare predictions from multiple models."""
        # Simulate model comparison logic
        return {
            "consensus": predictions[0]["value"] if predictions else None,
            "confidence": 0.87,
            "disagreement_areas": ["revenue_forecast", "churn_risk"]
        }
    
    tools = [
        # Different model endpoints
        {
            "type": "mcp",
            "server_label": "model_a",
            "server_url": "https://ml.company.com/model-a",
            "allowed_tools": ["predict", "explain"],
        },
        {
            "type": "mcp",
            "server_label": "model_b",
            "server_url": "https://ml.company.com/model-b",
            "allowed_tools": ["predict", "feature_importance"],
        },
        {
            "type": "function",
            "function": {
                "name": "compare_predictions",
                "description": "Compare predictions from multiple models",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "predictions": {
                            "type": "array",
                            "items": {"type": "object"}
                        }
                    }
                }
            },
            "implementation": compare_predictions
        },
        "web_search",  # For market context
        "code_interpreter"  # For statistical analysis
    ]
    
    analysis_task = """
    Perform comprehensive customer churn analysis:
    
    1. Load customer dataset from S3
    2. Preprocess data (handle missing values, encode categoricals)
    3. Get churn predictions from Model A
    4. Get churn predictions from Model B
    5. Compare model predictions and identify disagreements
    6. For high-disagreement cases, perform detailed feature analysis
    7. Search for industry churn benchmarks
    8. Generate ensemble prediction combining both models
    9. Create risk segments based on churn probability
    10. Generate actionable recommendations for each segment
    11. Create executive summary with key insights
    """
    
    plan = decompose(analysis_task, tools=tools)
    
    # Execute with custom configuration
    executor = Executor(
        max_concurrent=2,  # Run models in parallel
        timeout=600  # 10 minutes per step
    )
    
    results = executor.execute_plan(plan, run_id="churn_analysis_001")
    
    # Analyze execution metrics
    print("\n=== Execution Metrics ===")
    total_time = sum((r.completed_at - r.started_at).total_seconds() 
                    for r in results if r.completed_at)
    print(f"Total execution time: {total_time:.1f} seconds")
    print(f"Parallel speedup: {total_time / max(1, len(results)):.1f}x")


# Example 3: Event-Driven Workflow with Monitoring
async def event_driven_workflow():
    """
    Real-time event processing with monitoring and alerting.
    """
    print("\n=== Event-Driven Workflow ===")
    
    tools = [
        {
            "type": "mcp",
            "server_label": "event_stream",
            "server_url": "kafka://events.company.com:9092",
            "allowed_tools": ["consume_events", "produce_event"],
        },
        {
            "type": "mcp",
            "server_label": "monitoring",
            "server_url": "https://monitoring.company.com/api",
            "allowed_tools": ["log_metric", "create_alert", "check_threshold"],
        },
        {
            "type": "mcp",
            "server_label": "notification",
            "server_url": "https://notify.company.com/api",
            "allowed_tools": ["send_email", "send_slack", "send_sms"],
        },
        "code_interpreter"
    ]
    
    # Real-time event processing task
    event_task = """
    Process incoming payment events in real-time:
    
    1. Consume batch of payment events from Kafka
    2. Validate payment data integrity
    3. Check for fraud patterns using ML model
    4. For suspicious payments:
       - Create high-priority alert
       - Send notification to fraud team
       - Log detailed analysis
    5. For valid payments:
       - Process payment through payment gateway
       - Update customer balance
       - Send confirmation to customer
    6. Calculate real-time metrics:
       - Payment success rate
       - Average processing time
       - Fraud detection rate
    7. Check if metrics exceed thresholds
    8. If thresholds exceeded, trigger automated responses
    9. Generate hourly summary report
    """
    
    plan = decompose(event_task, tools=tools)
    
    # Execute with monitoring
    run_id = f"payment_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Custom executor with progress callback
    class MonitoredExecutor(Executor):
        async def on_step_complete(self, step_id: str, result: StepResult):
            """Called after each step completes."""
            if result.status == "completed":
                print(f"✓ Step {step_id}: Success")
                # Log metric to monitoring system
                await self.log_metric(f"step.{step_id}.duration", 
                                    (result.completed_at - result.started_at).total_seconds())
            else:
                print(f"✗ Step {step_id}: Failed - {result.error}")
                # Create alert for failed steps
                await self.create_alert(f"Step {step_id} failed", severity="high")
        
        async def log_metric(self, name: str, value: float):
            # Simulate metric logging
            pass
        
        async def create_alert(self, message: str, severity: str):
            # Simulate alert creation
            pass
    
    executor = MonitoredExecutor(max_concurrent=3)
    results = await executor.execute_plan_async(plan, run_id=run_id)


# Example 4: Complex Research Workflow
def research_workflow_example():
    """
    Multi-stage research workflow with iterative refinement.
    """
    print("\n=== Complex Research Workflow ===")
    
    # Research tools setup
    tools = [
        "web_search",
        {
            "type": "mcp",
            "server_label": "arxiv",
            "server_url": "https://arxiv.org/api/mcp",
            "allowed_tools": ["search_papers", "get_paper", "get_citations"],
        },
        {
            "type": "mcp",
            "server_label": "pubmed",
            "server_url": "https://pubmed.ncbi.nlm.nih.gov/api/mcp",
            "allowed_tools": ["search_articles", "get_abstract", "get_related"],
        },
        "code_interpreter",  # For data analysis
        {
            "type": "function",
            "function": {
                "name": "synthesize_findings",
                "description": "Synthesize research findings into coherent insights",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "findings": {"type": "array", "items": {"type": "object"}},
                        "focus_area": {"type": "string"}
                    }
                }
            },
            "implementation": lambda findings, focus_area: {
                "synthesis": "Comprehensive analysis of findings...",
                "key_insights": ["insight1", "insight2"],
                "confidence": 0.85
            }
        }
    ]
    
    # Multi-stage research task
    research_task = """
    Conduct comprehensive research on "AI applications in drug discovery":
    
    Phase 1 - Literature Review:
    1. Search ArXiv for recent papers on AI in drug discovery (last 2 years)
    2. Search PubMed for clinical applications
    3. Identify top 10 most cited papers
    4. Extract key methodologies and findings
    
    Phase 2 - Technology Analysis:
    5. Research current AI models used (transformers, GNNs, etc.)
    6. Compare performance metrics across different approaches
    7. Identify technology gaps and opportunities
    
    Phase 3 - Industry Analysis:
    8. Search for companies working in this space
    9. Analyze recent funding and partnerships
    10. Identify successful case studies
    
    Phase 4 - Synthesis:
    11. Synthesize all findings into key insights
    12. Create trend analysis with visualizations
    13. Generate future predictions
    14. Write executive summary
    15. Create detailed technical appendix
    """
    
    plan = decompose(research_task, tools=tools, max_steps=30)
    
    # Execute with phase tracking
    class PhaseTracker:
        def __init__(self):
            self.phases = {
                "Literature Review": ["1", "2", "3", "4"],
                "Technology Analysis": ["5", "6", "7"],
                "Industry Analysis": ["8", "9", "10"],
                "Synthesis": ["11", "12", "13", "14", "15"]
            }
            self.current_phase = None
        
        def track_progress(self, results: List[StepResult]):
            completed_steps = [r.step_id.split("_")[-1] for r in results 
                             if r.status == "completed"]
            
            for phase, steps in self.phases.items():
                phase_complete = all(s in completed_steps for s in steps)
                phase_progress = sum(1 for s in steps if s in completed_steps)
                
                print(f"{phase}: {phase_progress}/{len(steps)} steps " + 
                     ("✓" if phase_complete else "..."))
    
    # Execute with tracking
    tracker = PhaseTracker()
    run_id = "drug_discovery_research_001"
    
    # Execute in chunks for better control
    results = execute(plan, run_id=run_id)
    tracker.track_progress(results)
    
    print(f"\nResearch completed! Generated {len(results)} deliverables.")


# Example 5: Production Deployment Workflow
def deployment_workflow_example():
    """
    Automated deployment workflow with safety checks and rollback.
    """
    print("\n=== Production Deployment Workflow ===")
    
    tools = [
        {
            "type": "mcp",
            "server_label": "git",
            "server_url": "https://github.com/company/repo",
            "allowed_tools": ["checkout", "merge", "tag"],
        },
        {
            "type": "mcp",
            "server_label": "ci_cd",
            "server_url": "https://jenkins.company.com/api",
            "allowed_tools": ["run_tests", "build", "deploy", "rollback"],
        },
        {
            "type": "mcp",
            "server_label": "monitoring",
            "server_url": "https://datadog.company.com/api",
            "allowed_tools": ["check_metrics", "create_dashboard", "set_alert"],
        },
        {
            "type": "mcp",
            "server_label": "slack",
            "server_url": "https://slack.com/api/company",
            "allowed_tools": ["send_message", "create_thread"],
        }
    ]
    
    deployment_task = """
    Deploy version 2.5.0 to production with safety checks:
    
    Pre-deployment:
    1. Check out release branch 'release/2.5.0'
    2. Run full test suite
    3. Build Docker images
    4. Run security scan on images
    5. Generate deployment changelog
    
    Deployment:
    6. Deploy to staging environment
    7. Run smoke tests on staging
    8. Check staging metrics (response time, error rate)
    9. Get deployment approval (manual checkpoint)
    10. Deploy to production (blue-green deployment)
    11. Run production smoke tests
    
    Post-deployment:
    12. Monitor error rates for 15 minutes
    13. Monitor response times
    14. Check CPU and memory usage
    15. If any metric exceeds threshold:
        - Automatically rollback
        - Send alert to on-call
    16. If all metrics normal:
        - Switch all traffic to new version
        - Tag release in Git
        - Update deployment dashboard
        - Send success notification to #releases channel
    """
    
    plan = decompose(deployment_task, tools=tools)
    
    # Execute with safety controls
    executor = Executor(
        max_concurrent=1,  # Sequential for safety
        timeout=1800  # 30 minutes total
    )
    
    run_id = f"deploy_v2.5.0_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        results = executor.execute_plan(plan, run_id=run_id)
        
        # Check if deployment succeeded
        if all(r.status == "completed" for r in results):
            print("✓ Deployment successful!")
        else:
            print("✗ Deployment failed - automatic rollback initiated")
            
    except Exception as e:
        print(f"Deployment error: {e}")
        print("Initiating emergency rollback...")
        # Execute rollback plan
        rollback_plan = decompose("Emergency rollback to previous version", tools=tools)
        execute(rollback_plan, run_id=f"rollback_{run_id}")


if __name__ == "__main__":
    # Setup StepChain
    setup_stepchain()
    
    # Run examples
    data_pipeline_example()
    multi_model_analysis()
    
    # Run async example
    asyncio.run(event_driven_workflow())
    
    research_workflow_example()
    deployment_workflow_example()