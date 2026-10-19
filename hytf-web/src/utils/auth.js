import Cookies from 'js-cookie'
const CK = 'hytf_client_token'
const AK = 'hytf_admin_token'
const AIK = 'hytf_admin_info'
export const getClientToken = () => Cookies.get(CK) || ''
export const setClientToken = t => Cookies.set(CK, t, { expires: 0.5 })
export const removeClientToken = () => Cookies.remove(CK)
export const getAdminToken = () => sessionStorage.getItem(AK) || ''
export const setAdminToken = t => sessionStorage.setItem(AK, t)
export const removeAdminToken = () => sessionStorage.removeItem(AK)
export const getAdminInfo = () => {
  try { return JSON.parse(sessionStorage.getItem(AIK) || '{}') } catch (e) { return {} }
}
export const setAdminInfo = i => sessionStorage.setItem(AIK, JSON.stringify(i || {}))
export const removeAdminInfo = () => sessionStorage.removeItem(AIK)
