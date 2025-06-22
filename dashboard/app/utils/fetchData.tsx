"use client";

import { BodyData } from '../utils/dataTypes';

// Use HTTPS if your API supports it to avoid mixed content issues in browsers
const API_URL = 'https://api.danielle-pashayan.com/body_composition';

export async function fetchWeightData(): Promise<BodyData[]> {
    try {
        const response = await fetch(API_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: BodyData[] = await response.json();
        console.log('Weight data fetched successfully:', data);
        return data;
    } catch (error) {
        console.error('Error fetching weight data:', error);
        throw error;
    }
}