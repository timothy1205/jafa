import assert from "assert"

assert(process.env.REACT_APP_BACKEND_URL !== undefined)

const config = {
    "backend_url": process.env.REACT_APP_BACKEND_URL
}

export default config