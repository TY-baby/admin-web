import request from './request'
export const getCustomerList = params => request.get('/customers', { params })
export const createCustomer = data => request.post('/customers', data)
export const updateCustomer = (id, data) => request.put('/customers/' + id, data)
export const deleteCustomer = id => request.delete('/customers/' + id)
export const getCustomerDetail = id => request.get('/customers/' + id)
export const getContacts = customerId => request.get('/customers/' + customerId + '/contacts')
export const addContact = data => request.post('/customers/contacts', data)
