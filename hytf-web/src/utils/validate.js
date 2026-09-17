export const isPhone = v => /^1[3-9]\d{9}$/.test(v || '')
export const isPositiveInt = v => /^[1-9]\d*$/.test(String(v == null ? '' : v))
export const isPositiveNumber = v => /^\d+(\.\d{1,2})?$/.test(String(v == null ? '' : v)) && Number(v) > 0