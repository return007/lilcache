# lilcache

## Interprocess and thread safe light weight cache

**Note:**
This is under development and has bad performance (concurrency, response time, error prone, etc. you name it!). 
It is not ready for production use.  If you like taking risks, I won't stop you from using it.

## Timeline

 - [ ] Write unittests
 - [ ] Stress testing
 - [ ] Improve error handling
 - [ ] Extension to current implementation: Implement connection pool and client reuse connections
 - [ ] Implementation 2: Twisted bsaed concurrency
 - [ ] Implementation 3: Incordinated cache (file db + locks for synchronization)
 - [ ] For each implementation, perform benchmark tests and stress testing
 - [ ] Release to PyPi
 - [ ] Implementation 4: Named PIPE based approach and full duplex communication
 - [ ] Production ready code
