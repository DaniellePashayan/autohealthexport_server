import React, { createContext, useContext, useEffect, useState } from "react";

type DataType = any; // Replace with your actual data type

const DataContext = createContext<DataType | undefined>(undefined);

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState<DataType | null>(null);

  useEffect(() => {
    fetch("https://api.example.com/data")
      .then((res) => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
    <DataContext.Provider value={data}>{children}</DataContext.Provider>
  );
}

export function useData() {
  return useContext(DataContext);
}