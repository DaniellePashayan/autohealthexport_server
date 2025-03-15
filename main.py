from fastapi import FastAPI, HTTPException
from models.health_metrics import HealthRootModel
from database.database import connect_db, create_tables
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Auto Health Export sever application!"}

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
    create_tables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)