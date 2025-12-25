import { useMemo } from 'react';
import { env } from '../config/env';

/**
 * React hook to get the Google API key
 * @returns {string} The Google API key
 * @throws {Error} If the API key is not set
 */
export function useApiKey() {
  return useMemo(() => {
    return env.getGoogleApiKey();
  }, []);
}
