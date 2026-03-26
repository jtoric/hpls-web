/**
 * Shared formatting utilities.
 *
 * Pure helper functions used across multiple views and components
 * for consistent date and file-size display throughout the app.
 */

/** Croatian month names in genitive case (used by {@link formatDateCroatian}). */
const CROATIAN_MONTHS = [
  'siječnja', 'veljače', 'ožujka', 'travnja', 'svibnja', 'lipnja',
  'srpnja', 'kolovoza', 'rujna', 'listopada', 'studenoga', 'prosinca',
]

/**
 * Format an ISO date string as a Croatian long date.
 *
 * Uses the built-in `Intl.DateTimeFormat` via `toLocaleDateString`
 * for reliable locale-aware formatting.
 *
 * @param {string} dateStr - ISO 8601 date string (e.g. "2025-03-15T10:00:00Z").
 * @returns {string} Formatted date like "15. ožujka 2025." or empty string if falsy.
 */
export function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('hr-HR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

/**
 * Format an ISO date string as a Croatian date with genitive month names.
 *
 * Produces output like "15. ožujka 2025." matching Croatian grammar conventions.
 *
 * @param {string} dateStr - ISO 8601 date string.
 * @returns {string} Formatted date or empty string if falsy.
 */
export function formatDateCroatian(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const day = date.getDate()
  const month = CROATIAN_MONTHS[date.getMonth()]
  const year = date.getFullYear()
  return `${day}. ${month} ${year}.`
}

/**
 * Format a byte count into a human-readable size string.
 *
 * Divides by 1024 repeatedly until the value is below 1024,
 * then appends the appropriate unit (B, KB, MB, GB).
 *
 * @param {number} bytes - File size in bytes.
 * @returns {string} Formatted size like "2.4 MB" or empty string if falsy.
 */
export function formatFileSize(bytes) {
  if (!bytes) return ''
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  return `${size.toFixed(unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}
