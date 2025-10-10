import { useState, useEffect, useCallback, useRefe } from 'react'
import songsAPI from '../api/songs'

const useSongs = (options = {}) => {
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 20,
    total: 0,
    hasMore: false
  })
  
  const hasLoadedRef = useRef(false)

  const loadSongs = useCallback(async (newOptions = {}) => {
    if (loading && hasLoadedRef.current) return;

    try {
      setLoading(true);
      setError(null);

      const mergedOptions = { ...options, ...newOptions };
      const response = await songsAPI.getSongs(mergedOptions);

      if (response.results) {
        setSongs(response.results);
        setPagination({
          page: response.page || 1,
          pageSize: response.page_size || 20,
          total: response.count || 0,
          hasMore: response.next !== null,
        });
      } else {
        setSongs(Array.isArray(response) ? response : []);
        setPagination({
          page: 1,
          pageSize: 20,
          total: Array.isArray(response) ? response.length : 0,
          hasMore: false,
        });
      }

      hasLoadedRef.current = true;
    } catch (err) {
      setError(err.message || 'Failed to load songs');
      console.error('Error loading songs:', err);
    } finally {
      setLoading(false);
    }
  }, [options]); // ✅ include `options` here

  const loadMoreSongs = useCallback(async () => {
    if (loading || !pagination.hasMore) return
    
    try {
      setLoading(true)
      const nextPage = pagination.page + 1
      const response = await songsAPI.getSongs({ ...options, page: nextPage })
      
      if (response.results) {
        setSongs(prev => [...prev, ...response.results])
        setPagination(prev => ({
          ...prev,
          page: nextPage,
          hasMore: response.next !== null
        }))
      }
    } catch (err) {
      setError(err.message || 'Failed to load more songs')
      console.error('Error loading more songs:', err)
    } finally {
      setLoading(false)
    }
  }, [loading, pagination.hasMore, pagination.page, options])

  const searchSongs = useCallback(async (query, searchOptions = {}) => {
    if (!query.trim()) {
      return []
    }

    try {
      const response = await songsAPI.searchSongs(query, searchOptions)
      return response.results || response
    } catch (err) {
      console.error('Error searching songs:', err)
      return []
    }
  }, [])

  const refreshSongs = useCallback(async () => {
    hasLoadedRef.current = false
    await loadSongs()
  }, [loadSongs])

  const clearCache = useCallback(() => {
    songsAPI.clearCache()
  }, [])

  // Load songs only once on mount
  useEffect(() => {
    if (!hasLoadedRef.current && songs.length === 0) {
      loadSongs();
    }
  }, [loadSongs]); // ✅ include loadSongs




  return {
    songs,
    loading,
    error,
    pagination,
    loadSongs,
    loadMoreSongs,
    searchSongs,
    refreshSongs,
    clearCache
  }
}

export default useSongs
