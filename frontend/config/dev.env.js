'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BASE_ORIGIN: '"http://0.0.0.0:5577"',
  SECURE_COOKIE: false
})
