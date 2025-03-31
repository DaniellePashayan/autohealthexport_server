from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Table, MetaData, and_, desc
from sqlalchemy.dialects.postgresql import insert
from typing import Optional
import json
from datetime import datetime

from database.database import connect_db, create_tables
from models.health_metrics import HealthRootModel

app = FastAPI()

def get_metric_data(engine, metric_column):
    """
    Retrieves metric data from the database for a given column.
    """
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    
    with engine.connect() as conn:
        query = health_metrics_table.select().with_only_columns(
            health_metrics_table.c.date, metric_column
        )

        conditions = []
        try:
            if start_date := Query(None, description="Start date for filtering (YYYY-MM-DD)"): #using walrus operator
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                conditions.append(health_metrics_table.c.date >= start_datetime)
            if end_date := Query(None, description="End date for filtering (YYYY-MM-DD)"):
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
                end_datetime = datetime(end_datetime.year, end_datetime.month, end_datetime.day, 23, 59, 59)
                conditions.append(health_metrics_table.c.date <= end_datetime)
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if conditions:
            query = query.where(and_(*conditions))
            
        query = query.order_by(desc(health_metrics_table.c.date))
        results = conn.execute(query).fetchall()       
        metric_data = [{"date": row.date, str(metric_column.name): getattr(row, metric_column.name)} for row in results]
        return {"data": metric_data}

@app.get("/")
async def root():
    return {"message": "Welcome to the Auto Health Export sever application!"}

@app.get("/all_health_data")
async def get_health_data(
    start_date: Optional[str] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
):
    """
    Endpoint to retrieve health data from the database.
    """
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    
    with engine.connect() as conn:
        query = health_metrics_table.select()

        conditions = []
        try:
            if start_date:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                conditions.append(health_metrics_table.c.date >= start_datetime)
            if end_date:
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
                # Add a day to include the whole end date
                end_datetime = datetime(end_datetime.year, end_datetime.month, end_datetime.day, 23, 59, 59)
                conditions.append(health_metrics_table.c.date <= end_datetime)
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if conditions:
            query = query.where(and_(*conditions))
            
        query = query.order_by(desc(health_metrics_table.c.date)) # Order by date in descending order
        result = conn.execute(query)
        keys = result.keys() #get the keys from the result itself.
        result = result.fetchall() #get the result rows.
        
    data = [{key: row[i] for i, key in enumerate(keys)} for row in result]
    return {"data": data}


@app.get('/weight_data')
async def get_weight_data():
    """Endpoint to retrieve weight data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    return get_metric_data(engine, health_metrics_table.c.weight_body_mass)

@app.get('/steps_data')
async def get_steps_data():
    """Endpoint to retrieve steps data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    return get_metric_data(engine, health_metrics_table.c.step_count)  # Assuming 'steps' column exists



@app.post("/import_health_data")
async def import_healht_data(data: dict):
    """
    Endpoint to import health data.
    """
    data = json.loads(json.dumps(data))
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    parsed_data = HealthRootModel(**data)
    
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    valid_columns = set(health_metrics_table.columns.keys())
    
    rows = {}
    for metric in parsed_data.data.metrics:
        for data_point in metric.data:
            date = data_point.date
            if date not in rows:
                rows[date] = {"date": date}
            if metric.name in valid_columns:
                rows[date][metric.name] = data_point.qty
            
    # Filter out rows where all values (except date) are None
    filtered_rows = [
        row for row in rows.values()
        if any(value is not None for key, value in row.items() if key != "date")
    ]    
    
    with engine.connect() as conn:
        for row in filtered_rows:
            stmt = insert(health_metrics_table).values(row)
            stmt = stmt.on_conflict_do_update(
                index_elements=["date"],  # Primary key to check for conflicts
                set_={key: stmt.excluded[key] for key in row.keys() if key != "date"}
            )
            conn.execute(stmt)
            conn.commit()

    return {"message": "Data imported successfully", "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)
    create_tables()