import request from './request'
export const getWorkflowList = () => request.get('/workflows')
export const createWorkflow = data => request.post('/workflows', data)
export const updateWorkflow = (id, data) => request.put('/workflows/' + id, data)
export const deleteWorkflow = id => request.delete('/workflows/' + id)
export const getInstanceList = () => request.get('/workflows/instances')
export const createInstance = data => request.post('/workflows/instances', data)
export const approveInstance = (id, data) => request.post('/workflows/instances/' + id + '/approve', data)
