import Cookies from 'js-cookie'
const CK = 'hytf_client_token'
const AK = 'hytf_admin_token'
const AIK = 'hytf_admin_info'
export const getClientToken = () => Cookies.get(CK) || ''
export const setClientToken = t => Cookies.set(CK, t, { expires: 0.5 })
export const removeClientToken = () => Cookies.remove(CK)
export const getAdminToken = () => Cookies.get(AK) || ''
export const setAdminToken = t => Cookies.set(AK, t, { expires: 1 / 12 })
export const removeAdminToken = () => Cookies.remove(AK)
export const getAdminInfo = () => {
  try { return JSON.parse(localStorage.getItem(AIK) || '{}') } catch (e) { return {} }
}
export const setAdminInfo = i => localStorage.setItem(AIK, JSON.stringify(i || {}))
export const removeAdminInfo = () => localStorage.removeItem(AIK)
