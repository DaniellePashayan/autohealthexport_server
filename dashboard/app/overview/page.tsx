"use client";

import { fetchWeightData } from '../utils/fetchData';
import React, { useEffect, useState } from 'react';

const OverviewPage = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWeightData()
      .then((res) => setData(res))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  if (!data || data.length === 0) return <div>No data available.</div>;

  return (
    <table>
      <thead>
        <tr>
          {Object.keys(data[0]).map((key) => (
            <th key={key}>{key}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {Object.values(row).map((value, i) => (
              <td key={i}>{String(value)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OverviewPage;