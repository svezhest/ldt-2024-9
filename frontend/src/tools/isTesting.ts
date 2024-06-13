export const isTesting = () => {
  return process.env.NODE_ENV === 'development'
}
