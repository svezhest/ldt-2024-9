import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {App} from './App'
import React from 'react'

const rootElement = document.getElementById('root')
// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const root = createRoot(rootElement!)

root.render(
  <StrictMode>
    <App />
  </StrictMode>
)
