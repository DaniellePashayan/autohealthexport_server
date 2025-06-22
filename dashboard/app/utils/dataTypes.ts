export interface ActivityData {
  date: string;
  stand_time: number; // in minutes
  stand_hours: number; // in hours
  exerciseTime: number; // in minutes
  flightsClimbed: number; // number of flights
  steps: number;
  distance: number; // in miles
}

export interface NutritionData {
  date: string;
  caloriesConsumed: number;
  carbs: number; // in grams
  cholesterol: number; // in mg
  calcium: number; // in mg
  sugar: number; // in grams
  folate: number; // in mcg
  fiber: number; // in grams
  iron: number; // in mg
  magnesium: number; // in mg
  monoUnsaturatedFat: number; // in grams
  niacin: number; // in mg
  potassium: number; // in mg
  riboflavin: number; // in mg
  protein: number; // in grams
  saturatedFat: number; // in grams
  sodium: number; // in mg
  thiamin: number; // in mg
  totalFat: number; // in grams
  vitaminB6: number; // in mg
  vitaminA: number; // in mg
  vitaminC: number; // in mg
  vitaminB12: number; // in mcg
  zinc: number; // in mg
}

export interface BodyData {
  date: string;
  weight: number; // in lbs
  bodyMassIndex: number; // BMI
  bodyFatPercentage: number; // in percentage
  leanBodyMass: number; // in lbs
}
