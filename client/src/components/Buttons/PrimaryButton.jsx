import React from 'react'

const PrimaryButton = ({ 
  children, 
  onClick, 
  disabled = false, 
  size = 'md',
  className = '',
  type = 'button',
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
  
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  }
  
  const colorClasses = 'bg-pink-500 hover:bg-pink-600 text-white focus:ring-pink-500 shadow-lg hover:shadow-xl hover:shadow-pink-500/25'
  
  const classes = `${baseClasses} ${sizeClasses[size]} ${colorClasses} ${className}`

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  )
}

export default PrimaryButton
