import { RenderData, Streamlit } from "streamlit-component-lib"

declare global {
  interface Window {
    Streamlit: any
  }
}

window.Streamlit = Streamlit

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
async function onRender(event: Event) {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  const body: string = data.args["body"]
  const style: string = data.args["style"]
  window.document.body.innerHTML = body;
  var styleSheet = document.createElement("style")
  styleSheet.textContent = style
  document.head.appendChild(styleSheet)
  Streamlit.setFrameHeight()
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
