// pages/_app.js
import {NextUIProvider} from '@nextui-org/react'
import React from 'react';

function MyApp({ Component, pageProps }) {
  return (
    <React.StrictMode>
      <NextUIProvider>
        <Component {...pageProps} />
      </NextUIProvider>
    </React.StrictMode>
  )
}

export default MyApp;