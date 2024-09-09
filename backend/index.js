const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

var Main = require('./routes/Main')

var app = express()
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));
app.use(cors({origin:'*'}))
app.listen(3500,()=>console.log('Server started at : 3500'))

app.use('/Main',Main)
app.use(express.static('public'))