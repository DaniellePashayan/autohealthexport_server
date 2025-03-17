from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    """
    Connect to the PostgreSQL database using SQLAlchemy.
    """
    # Database connection URL
    db_url = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT 1 FROM health_metrics LIMIT 1;"))  # Quick check
        except ProgrammingError:
            print("Table 'health_metrics' not found. Creating tables...")
            create_tables(engine)  # Call create_tables() if the table does not exist
    
    return engine
    
def create_tables(engine):
    """
    Create all tables in the database if they do not exist.
    """
   
    # Health Metrics table
    health_metrics_table_query = text("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        date TIMESTAMP PRIMARY KEY,
        apple_stand_time FLOAT,
        apple_stand_hour FLOAT,
        body_mass_index FLOAT,
        active_energy FLOAT,
        apple_exercise_time FLOAT,
        carbohydrates FLOAT,
        body_fat_percentage FLOAT,
        blood_oxygen_saturation FLOAT,
        cholesterol FLOAT,
        calcium FLOAT,
        dietary_sugar FLOAT,
        dietary_energy FLOAT,
        flights_climbed FLOAT,
        folate FLOAT,
        fiber FLOAT,
        heart_rate FLOAT,
        heart_rate_variability FLOAT,
        heart_rate_avg FLOAT,
        heart_rate_min FLOAT,
        heart_rate_max FLOAT,
        iron FLOAT,
        magnesium FLOAT,
        monounsaturated_fat FLOAT,
        niacin FLOAT,
        headphone_audio_exposure FLOAT,
        lean_body_mass FLOAT,
        polyunsaturated_fat FLOAT,
        potassium FLOAT,
        basal_energy_burned FLOAT,
        riboflavin FLOAT,
        resting_heart_rate FLOAT,
        respiratory_rate FLOAT,
        protein FLOAT,
        saturated_fat FLOAT,
        sleep_analysis FLOAT,
        sodium FLOAT,
        step_count FLOAT,
        time_in_daylight FLOAT,
        thiamin FLOAT,
        total_fat FLOAT,
        stair_speed_up FLOAT,
        vitamin_b6 FLOAT,
        stair_speed_down FLOAT,
        vitamin_a FLOAT,
        vitamin_c FLOAT,
        vitamin_b12 FLOAT,
        walking_running_distance FLOAT,
        walking_heart_rate_average FLOAT,
        zinc FLOAT,
        walking_double_support_percentage FLOAT,
        walking_asymmetry_percentage FLOAT,
        weight_body_mass FLOAT,
        walking_speed FLOAT,
        walking_step_length FLOAT
    );
    """)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    with session.begin():
        # Execute all table creation queries
        session.execute(health_metrics_table_query)
        session.commit()

    print("All tables created successfully.")

# Call the function to create tables
if __name__ == "__main__":
    create_tables()