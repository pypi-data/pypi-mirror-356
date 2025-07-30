"""
DataIntelligenceHub: A unified interface showcasing defog-python capabilities
"""
import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Union, Literal
from pathlib import Path
import pandas as pd
import duckdb
from pydantic import BaseModel, Field

from defog.llm import chat_async
from defog.sql_agent import SQLAgent
from defog.pdf_data_extractor import PDFDataExtractor
from defog.image_data_extractor import ImageDataExtractor
from defog.html_data_extractor import HTMLDataExtractor
from defog.text_data_extractor import TextDataExtractor
from defog.enhanced_agent_orchestrator import EnhancedAgentOrchestrator
from defog.agents.base_agent import BaseAgent
from defog.providers import get_appropriate_provider
from defog.memory import MemoryManager
from defog.providers.providers import Provider


class QueryResult(BaseModel):
    """Structured result from database queries"""
    query: str
    data: List[Dict[str, Any]]
    row_count: int
    execution_time: float
    natural_language_summary: Optional[str] = None


class ExtractionResult(BaseModel):
    """Structured result from data extraction"""
    source: str
    source_type: Literal["pdf", "image", "html", "text"]
    extracted_data: List[Dict[str, Any]]
    schema: Dict[str, Any]
    confidence: float
    extraction_time: float


class DataIntelligenceHub:
    """
    A unified interface demonstrating defog-python capabilities.
    Combines LLM operations, data extraction, SQL generation, and agent orchestration.
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        database_path: str = "demo_data.db",
        enable_thinking: bool = False,
        verbose: bool = True
    ):
        """
        Initialize the DataIntelligenceHub.
        
        Args:
            provider: LLM provider (openai, anthropic, gemini, together)
            model: Specific model to use (defaults to provider's best model)
            api_key: API key for the provider
            database_path: Path to DuckDB database file
            enable_thinking: Enable thinking mode for complex reasoning
            verbose: Print progress and debug information
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.database_path = database_path
        self.enable_thinking = enable_thinking
        self.verbose = verbose
        
        # Initialize components
        self.memory_manager = MemoryManager()
        self.sql_agent = None
        self.orchestrator = None
        self._setup_database()
        
        # Track costs
        self.total_cost = 0.0
        self.operation_history = []
        
    def _setup_database(self):
        """Initialize DuckDB connection"""
        self.db = duckdb.connect(self.database_path)
        if self.verbose:
            print(f"Connected to database: {self.database_path}")
    
    def configure(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        enable_thinking: Optional[bool] = None,
        memory_strategy: Optional[str] = None
    ):
        """
        Reconfigure the hub with new settings.
        
        Args:
            provider: New LLM provider
            model: New model
            enable_thinking: Enable/disable thinking mode
            memory_strategy: Memory compactification strategy
        """
        if provider:
            self.provider = provider
            self.api_key = os.getenv(f"{provider.upper()}_API_KEY")
        if model:
            self.model = model
        if enable_thinking is not None:
            self.enable_thinking = enable_thinking
        if memory_strategy:
            self.memory_manager.strategy = memory_strategy
            
        if self.verbose:
            print(f"Configuration updated: provider={self.provider}, model={self.model}")
    
    async def chat(
        self,
        message: str,
        temperature: float = 0.7,
        response_format: Optional[BaseModel] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Union[str, BaseModel, Dict[str, Any]]:
        """
        Simple chat interface with automatic provider handling.
        
        Args:
            message: User message
            temperature: LLM temperature
            response_format: Pydantic model for structured output
            tools: List of tools available to the LLM
            stream: Enable streaming responses
            
        Returns:
            LLM response (string, structured object, or tool calls)
        """
        # Add to memory
        self.memory_manager.add_message("user", message)
        
        # Get appropriate provider
        provider_instance = get_appropriate_provider(
            provider=self.provider,
            model=self.model,
            api_key=self.api_key
        )
        
        # Prepare messages with memory
        messages = self.memory_manager.get_messages_for_api()
        
        # Call LLM
        response = await chat_async(
            messages=messages,
            provider=provider_instance,
            temperature=temperature,
            response_format=response_format,
            tools=tools,
            stream=stream,
            reasoning_effort="high" if self.enable_thinking else None
        )
        
        # Track response
        self.memory_manager.add_message("assistant", response)
        
        # Track cost (simplified - would need actual cost calculation)
        self._track_operation("chat", {"message": message, "response": response})
        
        return response
    
    async def extract_data(
        self,
        source: Union[str, Path],
        source_type: Optional[Literal["pdf", "image", "html", "text"]] = None,
        custom_schema: Optional[BaseModel] = None,
        parallel: bool = True
    ) -> ExtractionResult:
        """
        Extract structured data from various sources.
        
        Args:
            source: Path to file or text content
            source_type: Type of source (auto-detected if not provided)
            custom_schema: Custom Pydantic schema for extraction
            parallel: Use parallel processing for PDFs
            
        Returns:
            ExtractionResult with extracted data
        """
        import time
        start_time = time.time()
        
        # Auto-detect source type if not provided
        if source_type is None:
            if isinstance(source, Path) or (isinstance(source, str) and os.path.exists(source)):
                ext = Path(source).suffix.lower()
                if ext == ".pdf":
                    source_type = "pdf"
                elif ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
                    source_type = "image"
                elif ext in [".html", ".htm"]:
                    source_type = "html"
                else:
                    source_type = "text"
            else:
                source_type = "text"
        
        # Select appropriate extractor
        if source_type == "pdf":
            extractor = PDFDataExtractor(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            result = await extractor.extract(
                str(source),
                output_type=custom_schema,
                parallel=parallel
            )
        
        elif source_type == "image":
            extractor = ImageDataExtractor(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            result = await extractor.extract(
                str(source),
                output_type=custom_schema
            )
        
        elif source_type == "html":
            extractor = HTMLDataExtractor(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            result = await extractor.extract(
                str(source),
                output_type=custom_schema
            )
        
        else:  # text
            extractor = TextDataExtractor(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
            result = await extractor.extract(
                source if isinstance(source, str) else Path(source).read_text(),
                output_type=custom_schema
            )
        
        # Format result
        extraction_result = ExtractionResult(
            source=str(source),
            source_type=source_type,
            extracted_data=result if isinstance(result, list) else [result],
            schema=custom_schema.model_json_schema() if custom_schema else {},
            confidence=0.95,  # Simplified - would calculate actual confidence
            extraction_time=time.time() - start_time
        )
        
        self._track_operation("extract_data", {
            "source": str(source),
            "source_type": source_type,
            "row_count": len(extraction_result.extracted_data)
        })
        
        return extraction_result
    
    async def load_to_database(
        self,
        data: Union[List[Dict], pd.DataFrame, ExtractionResult],
        table_name: str,
        if_exists: Literal["fail", "replace", "append"] = "replace"
    ) -> int:
        """
        Load data into DuckDB database.
        
        Args:
            data: Data to load (list of dicts, DataFrame, or ExtractionResult)
            table_name: Name of table to create/append
            if_exists: How to handle existing table
            
        Returns:
            Number of rows loaded
        """
        # Convert to DataFrame
        if isinstance(data, ExtractionResult):
            df = pd.DataFrame(data.extracted_data)
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # Load to DuckDB
        if if_exists == "replace":
            self.db.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
        
        row_count = len(df)
        if self.verbose:
            print(f"Loaded {row_count} rows into table '{table_name}'")
        
        self._track_operation("load_to_database", {
            "table_name": table_name,
            "row_count": row_count
        })
        
        return row_count
    
    async def query_database(
        self,
        natural_language_query: str,
        return_summary: bool = True
    ) -> QueryResult:
        """
        Query database using natural language.
        
        Args:
            natural_language_query: Natural language query
            return_summary: Generate natural language summary of results
            
        Returns:
            QueryResult with data and optional summary
        """
        import time
        start_time = time.time()
        
        # Initialize SQL agent if needed
        if self.sql_agent is None:
            self.sql_agent = SQLAgent(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key,
                db_type="duckdb",
                db_conn=self.db
            )
        
        # Generate and execute SQL
        sql = await self.sql_agent.generate_sql(natural_language_query)
        result = self.db.execute(sql).fetchall()
        columns = [desc[0] for desc in self.db.description]
        
        # Convert to list of dicts
        data = [dict(zip(columns, row)) for row in result]
        
        # Generate summary if requested
        summary = None
        if return_summary and data:
            summary_prompt = f"""
            The user asked: "{natural_language_query}"
            
            The SQL query returned {len(data)} rows.
            First few rows: {json.dumps(data[:3], indent=2)}
            
            Provide a brief natural language summary of the results.
            """
            summary = await self.chat(summary_prompt)
        
        query_result = QueryResult(
            query=sql,
            data=data,
            row_count=len(data),
            execution_time=time.time() - start_time,
            natural_language_summary=summary
        )
        
        self._track_operation("query_database", {
            "natural_language": natural_language_query,
            "sql": sql,
            "row_count": len(data)
        })
        
        return query_result
    
    async def solve_complex_task(
        self,
        task_description: str,
        available_tools: Optional[List[str]] = None,
        max_thinking_time: int = 30000,
        explore_alternatives: bool = True
    ) -> Dict[str, Any]:
        """
        Solve complex tasks using multi-agent orchestration.
        
        Args:
            task_description: Description of the task
            available_tools: List of tools agents can use
            max_thinking_time: Max milliseconds for thinking
            explore_alternatives: Explore multiple solution paths
            
        Returns:
            Solution with steps, results, and artifacts
        """
        # Initialize orchestrator if needed
        if self.orchestrator is None:
            self.orchestrator = EnhancedAgentOrchestrator(
                provider=self.provider,
                model=self.model,
                api_key=self.api_key,
                enable_thinking=self.enable_thinking,
                shared_memory_dir="./agent_workspace"
            )
        
        # Define specialized agents
        agents = [
            BaseAgent(
                name="Researcher",
                role="Research and gather information",
                goal="Find relevant information and context",
                backstory="Expert at finding and synthesizing information",
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            ),
            BaseAgent(
                name="Analyst",
                role="Analyze data and provide insights",
                goal="Extract meaningful insights from data",
                backstory="Data analysis and pattern recognition expert",
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            ),
            BaseAgent(
                name="Builder",
                role="Create solutions and implementations",
                goal="Build working solutions",
                backstory="Expert at creating practical implementations",
                provider=self.provider,
                model=self.model,
                api_key=self.api_key
            )
        ]
        
        # Add agents to orchestrator
        for agent in agents:
            self.orchestrator.add_agent(agent)
        
        # Create task plan
        plan = f"""
        Task: {task_description}
        
        Please solve this task by:
        1. Understanding the requirements
        2. Breaking it down into subtasks
        3. Delegating to appropriate agents
        4. Synthesizing the results
        
        Available tools: {available_tools or ['research', 'analyze', 'build']}
        """
        
        # Execute with orchestrator
        result = await self.orchestrator.execute(
            plan,
            thinking_time=max_thinking_time,
            explore_alternatives=explore_alternatives
        )
        
        self._track_operation("solve_complex_task", {
            "task": task_description,
            "agents_used": len(agents),
            "success": result.get("success", False)
        })
        
        return result
    
    def create_data_pipeline(
        self,
        sources: List[Dict[str, Any]],
        transformations: Optional[List[callable]] = None,
        destination_table: str = "pipeline_output"
    ) -> Dict[str, Any]:
        """
        Create a data pipeline from extraction to database.
        
        Args:
            sources: List of source configurations
            transformations: Optional data transformations
            destination_table: Output table name
            
        Returns:
            Pipeline execution summary
        """
        async def run_pipeline():
            all_data = []
            
            for source_config in sources:
                # Extract data
                result = await self.extract_data(
                    source=source_config["path"],
                    source_type=source_config.get("type"),
                    custom_schema=source_config.get("schema")
                )
                all_data.extend(result.extracted_data)
            
            # Apply transformations
            if transformations:
                df = pd.DataFrame(all_data)
                for transform in transformations:
                    df = transform(df)
                all_data = df.to_dict("records")
            
            # Load to database
            rows_loaded = await self.load_to_database(
                all_data,
                destination_table
            )
            
            return {
                "sources_processed": len(sources),
                "total_rows": rows_loaded,
                "destination_table": destination_table
            }
        
        return asyncio.run(run_pipeline())
    
    def show_capabilities(self) -> Dict[str, List[str]]:
        """Show available capabilities of the hub"""
        return {
            "providers": ["openai", "anthropic", "gemini", "together"],
            "extraction_types": ["pdf", "image", "html", "text"],
            "database_operations": ["natural_language_query", "load_data", "export_data"],
            "agent_capabilities": ["research", "analysis", "building", "exploration"],
            "advanced_features": ["thinking_mode", "memory_management", "cost_tracking", "parallel_processing"]
        }
    
    def estimate_cost(self, operation: str, **kwargs) -> Dict[str, float]:
        """Estimate cost for an operation"""
        # Simplified cost estimation
        base_costs = {
            "chat": 0.01,
            "extract_pdf": 0.05,
            "extract_image": 0.02,
            "query_database": 0.01,
            "solve_complex_task": 0.10
        }
        
        base = base_costs.get(operation, 0.02)
        
        # Adjust based on parameters
        if operation == "extract_pdf" and kwargs.get("page_count", 1) > 10:
            base *= kwargs["page_count"] / 10
        
        if operation == "solve_complex_task" and kwargs.get("explore_alternatives"):
            base *= 2
        
        return {
            "estimated_cost": base,
            "provider": self.provider,
            "factors": kwargs
        }
    
    def get_operation_history(self) -> List[Dict[str, Any]]:
        """Get history of operations performed"""
        return self.operation_history
    
    def _track_operation(self, operation: str, details: Dict[str, Any]):
        """Track operations for history and cost"""
        self.operation_history.append({
            "operation": operation,
            "details": details,
            "timestamp": pd.Timestamp.now().isoformat(),
            "provider": self.provider
        })
        
        # Update total cost (simplified)
        self.total_cost += self.estimate_cost(operation, **details)["estimated_cost"]
    
    def export_results(self, format: Literal["json", "csv", "parquet"] = "json") -> str:
        """Export all data and results"""
        export_data = {
            "operation_history": self.operation_history,
            "total_cost": self.total_cost,
            "tables": {}
        }
        
        # Get all tables from database
        tables = self.db.execute("SHOW TABLES").fetchall()
        for table in tables:
            table_name = table[0]
            df = self.db.execute(f"SELECT * FROM {table_name}").df()
            export_data["tables"][table_name] = df.to_dict("records")
        
        # Export based on format
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        if format == "json":
            filename = f"export_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(export_data, f, indent=2, default=str)
        
        elif format == "csv":
            # Export tables as separate CSVs
            for table_name, data in export_data["tables"].items():
                df = pd.DataFrame(data)
                df.to_csv(f"export_{table_name}_{timestamp}.csv", index=False)
            filename = f"export_{timestamp}_tables.csv"
        
        else:  # parquet
            filename = f"export_{timestamp}.parquet"
            # Would implement parquet export
        
        return filename
    
    def __repr__(self):
        return f"DataIntelligenceHub(provider={self.provider}, model={self.model}, database={self.database_path})"