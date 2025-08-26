import React, { useEffect, useRef } from 'react'
import { fetchGoogleAdsConfig, trackAdImpression } from '../../api/ads'

const GoogleAdSlot = ({ 
  slotId, 
  format = 'auto', 
  responsive = true, 
  className = '',
  onAdLoad = () => {},
  onAdError = () => {}
}) => {
  const adRef = useRef(null)
  const adLoaded = useRef(false)

  useEffect(() => {
    const loadAd = async () => {
      try {
        // Fetch ad configuration from API
        const config = await fetchGoogleAdsConfig(slotId, { format, responsive })
        
        if (config && config.enabled && window.googletag) {
          // Initialize Google Ad
          window.googletag.cmd.push(() => {
            const adSlot = window.googletag.defineSlot(
              config.adUnit,
              config.sizes,
              slotId
            )
            
            if (adSlot) {
              // Add event listeners
              window.googletag.pubads().addEventListener('slotRenderEnded', (event) => {
                if (event.slot === adSlot) {
                  adLoaded.current = true
                  onAdLoad(event)
                  
                  // Track impression
                  if (config.trackImpression) {
                    trackAdImpression(config.adId, {
                      slot: slotId,
                      format,
                      responsive
                    })
                  }
                }
              })
              
              window.googletag.pubads().addEventListener('slotRequested', (event) => {
                if (event.slot === adSlot) {
                  // Ad request started
                }
              })
              
              window.googletag.pubads().addEventListener('slotResponseReceived', (event) => {
                if (event.slot === adSlot) {
                  // Ad response received
                }
              })
              
              // Enable services
              window.googletag.pubads().enableSingleRequest()
              window.googletag.pubads().collapseEmptyDivs()
              
              // Display the ad
              window.googletag.display(slotId)
              window.googletag.pubads().refresh([adSlot])
            }
          })
        } else {
          // Fallback content when ads are disabled or Google Ads not available
          if (adRef.current) {
            adRef.current.innerHTML = `
              <div class="bg-gray-200 rounded-lg p-4 text-center text-gray-500">
                <p class="text-sm">Advertisement</p>
                <div class="bg-gray-300 rounded h-16 flex items-center justify-center mt-2">
                  <span class="text-xs">Ad Space</span>
                </div>
              </div>
            `
          }
        }
      } catch (error) {
        console.error(`Error loading Google Ad for slot ${slotId}:`, error)
        onAdError(error)
        
        // Show fallback content
        if (adRef.current) {
          adRef.current.innerHTML = `
            <div class="bg-gray-200 rounded-lg p-4 text-center text-gray-500">
              <p class="text-sm">Advertisement</p>
              <div class="bg-gray-300 rounded h-16 flex items-center justify-center mt-2">
                <span class="text-xs">Ad Unavailable</span>
              </div>
            </div>
          `
        }
      }
    }

    // Load ad when component mounts
    loadAd()

    // Cleanup function
    return () => {
      if (window.googletag && adLoaded.current) {
        window.googletag.cmd.push(() => {
          window.googletag.destroySlots()
        })
      }
    }
  }, [slotId, format, responsive, onAdLoad, onAdError])

  return (
    <div 
      ref={adRef}
      id={slotId}
      className={`google-ad-slot ${className}`}
      style={{ minHeight: '90px' }}
    >
      {/* Loading state */}
      <div className="bg-gray-100 rounded-lg p-4 text-center text-gray-400">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-24 mx-auto mb-2"></div>
          <div className="h-16 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  )
}

export default GoogleAdSlot
