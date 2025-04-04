from fastapi import FastAPI, HTTPException
from sqlalchemy import Table, MetaData, desc
from sqlalchemy.dialects.postgresql import insert
from typing import List
import json

from database.database import connect_db, create_tables
from models.health_metrics import HealthRootModel

app = FastAPI()

def get_metric_data(engine, table, metric_columns: List):
    """
    Retrieves metric data from the database for a given column.
    """

    with engine.connect() as conn:
        query = table.select().with_only_columns(
            table.c.date, *metric_columns
        )

        query = query.order_by(desc(table.c.date))
        results = conn.execute(query).fetchall()       
        metric_data = [dict(row._mapping) for row in results]
        return {"data": metric_data}

@app.get("/")
async def root():
    return {"message": "Welcome to the Auto Health Export server application!"}

@app.get("/all_health_data", tags=['General'])
async def get_health_data():
    """
    Endpoint to retrieve health data from the database.
    """
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    
    with engine.connect() as conn:
        query = health_metrics_table.select()
            
        query = query.order_by(desc(health_metrics_table.c.date))
        result = conn.execute(query)
        keys = result.keys()
        result = result.fetchall()
        
    data = [{key: row[i] for i, key in enumerate(keys)} for row in result]
    return {"data": data}

# ------------ BODY METRICS ------------
@app.get('/weight', tags=['Body'])
async def get_weight_data():
    """Endpoint to retrieve weight data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    return get_metric_data(engine, health_metrics_table, [health_metrics_table.c.weight_body_mass])

@app.get('/body_composition', tags=['Body'])
async def get_body_composition_data():
    """Endpoint to retrieve body composition data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    columns = [
        health_metrics_table.c.weight_body_mass,
        health_metrics_table.c.body_mass_index,
        health_metrics_table.c.body_fat_percentage,
        health_metrics_table.c.lean_body_mass
    ]
    return get_metric_data(engine, health_metrics_table, columns)


@app.get('/heart_rate', tags=['Body'])
async def get_heart_rate_data():
    """Endpoint to retrieve heart rate data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    columns = [
        health_metrics_table.c.heart_rate,
        health_metrics_table.c.heart_rate_variability,
        health_metrics_table.c.heart_rate_avg,
        health_metrics_table.c.heart_rate_min,
        health_metrics_table.c.heart_rate_max
    ]
    return get_metric_data(engine, health_metrics_table, columns)

# ------------ ACTIVITY METRICS ------------
@app.get('/steps', tags=['Activity'])
async def get_steps_data():
    """Endpoint to retrieve steps data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    return get_metric_data(engine, health_metrics_table, [health_metrics_table.c.step_count])

@app.get('/exercise', tags=['Activity'])
async def get_exercise_data():
    """Endpoint to retrieve exercise and movement data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    columns = [
        health_metrics_table.c.apple_stand_time,
        health_metrics_table.c.apple_stand_hour,
        health_metrics_table.c.apple_exercise_time,
        health_metrics_table.c.flights_climbed,
        health_metrics_table.c.step_count,
        health_metrics_table.c.walking_running_distance
    ]
    return get_metric_data(engine, health_metrics_table, columns)

# ------------ NUTRITION METRICS ------------
@app.get('/nutrition', tags=['Nutrition'])
async def get_nutrition_data():
    """Endpoint to retrieve nutrition data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    columns = [
        health_metrics_table.c.dietary_energy,
        health_metrics_table.c.carbohydrates,
        health_metrics_table.c.cholesterol,
        health_metrics_table.c.calcium,
        health_metrics_table.c.dietary_sugar,
        health_metrics_table.c.folate,
        health_metrics_table.c.fiber,
        health_metrics_table.c.iron,
        health_metrics_table.c.magnesium,
        health_metrics_table.c.monounsaturated_fat,
        health_metrics_table.c.niacin,
        health_metrics_table.c.potassium,
        health_metrics_table.c.riboflavin,
        health_metrics_table.c.protein,
        health_metrics_table.c.saturated_fat,
        health_metrics_table.c.sodium,
        health_metrics_table.c.thiamin,
        health_metrics_table.c.total_fat,
        health_metrics_table.c.vitamin_b6,
        health_metrics_table.c.vitamin_a,
        health_metrics_table.c.vitamin_c,
        health_metrics_table.c.vitamin_b12,
        health_metrics_table.c.zinc
    ]
    return get_metric_data(engine, health_metrics_table, columns)

@app.get('/CICO', tags=['Nutrition'])
async def get_cico_data():
    """Endpoint to retrieve calories in vs calories out data."""
    engine = connect_db()
    metadata = MetaData()
    health_metrics_table = Table("health_metrics", metadata, autoload_with=engine)
    columns = [
        health_metrics_table.c.dietary_energy,
        health_metrics_table.c.active_energy,
        health_metrics_table.c.basal_energy_burned
    ]
    return get_metric_data(engine, health_metrics_table, columns)

# ------------ IMPORT DATA ------------
@app.post("/import_health_data", tags=['Import'])
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