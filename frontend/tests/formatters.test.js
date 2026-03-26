/**
 * Unit tests for shared formatting utilities.
 */
import { describe, it, expect } from 'vitest'
import { formatDate, formatDateCroatian, formatFileSize } from '../src/utils/formatters'

// ---------------------------------------------------------------------------
// formatDate
// ---------------------------------------------------------------------------
describe('formatDate', () => {
  it('returns empty string for falsy input', () => {
    expect(formatDate('')).toBe('')
    expect(formatDate(null)).toBe('')
    expect(formatDate(undefined)).toBe('')
  })

  it('formats an ISO date string in Croatian locale', () => {
    const result = formatDate('2025-03-15T10:00:00Z')
    // Should contain "2025" and "15" — exact month name depends on locale data
    expect(result).toContain('2025')
    expect(result).toContain('15')
  })
})

// ---------------------------------------------------------------------------
// formatDateCroatian
// ---------------------------------------------------------------------------
describe('formatDateCroatian', () => {
  it('returns empty string for falsy input', () => {
    expect(formatDateCroatian('')).toBe('')
    expect(formatDateCroatian(null)).toBe('')
  })

  it('formats date with Croatian genitive month names', () => {
    const result = formatDateCroatian('2025-01-05T12:00:00Z')
    expect(result).toContain('5.')
    expect(result).toContain('siječnja')
    expect(result).toContain('2025')
  })

  it('handles December correctly', () => {
    const result = formatDateCroatian('2024-12-25T00:00:00Z')
    expect(result).toContain('prosinca')
    expect(result).toContain('2024')
  })
})

// ---------------------------------------------------------------------------
// formatFileSize
// ---------------------------------------------------------------------------
describe('formatFileSize', () => {
  it('returns empty string for falsy input', () => {
    expect(formatFileSize(0)).toBe('')
    expect(formatFileSize(null)).toBe('')
    expect(formatFileSize(undefined)).toBe('')
  })

  it('formats bytes', () => {
    expect(formatFileSize(500)).toBe('500 B')
  })

  it('formats kilobytes', () => {
    expect(formatFileSize(1024)).toBe('1.0 KB')
    expect(formatFileSize(2560)).toBe('2.5 KB')
  })

  it('formats megabytes', () => {
    expect(formatFileSize(1048576)).toBe('1.0 MB')
    expect(formatFileSize(5242880)).toBe('5.0 MB')
  })

  it('formats gigabytes', () => {
    expect(formatFileSize(1073741824)).toBe('1.0 GB')
  })
})
