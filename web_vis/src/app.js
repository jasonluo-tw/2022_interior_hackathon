const path = require('path')
const express = require('express')
const hbs = require('hbs')

const app = express()

// Define path for express config
const distDirectoryPath = path.join(__dirname, '../dist')
const viewsPath = path.join(__dirname, '../templates/views')
const partialsPath = path.join(__dirname, '../templates/partials')

// Set up handlebars engine and views location
app.set('view engine', 'hbs')
app.set('views', viewsPath)
hbs.registerPartials(partialsPath)

// Set up public path
app.use(express.static(distDirectoryPath))

app.listen(3000, () => {
    console.log('Server is up on port 3000')
})