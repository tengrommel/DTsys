package main

import (
  "log"
  "net/http"
  "os"
)

func main()  {
  mux := http.NewServeMux()

  wd, err := os.Getwd()
  if err != nil{
    log.Fatal(err)
  }
  mux.Handle("/static/", http.StripPrefix("/static/",
    http.FileServer(http.Dir(wd))))

  err = http.ListenAndServe(":8080", mux)
  if err != nil{
    log.Fatal(err)
  }

}


