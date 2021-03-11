import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

//const API_URL = 'http://localhost:8080/api/test/';
const API_URL = '/api/';
//const API_URL = '/';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }
  // a get request to Django that has a template containing csrf token will set the token in the cookie
  // this is needed for Django to handle api calls from the browser
  setCSRFToken(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

  // below are just testing for getting contents from the backend
  getPublicContent(): Observable<any> {
    return this.http.get(API_URL + 'all', { responseType: 'text' });
  }

  getUserBoard(): Observable<any> {
    return this.http.get(API_URL + 'user', { responseType: 'text' });
  }

  getROBoard(): Observable<any> {
    return this.http.get(API_URL + 'ro', { responseType: 'text' });
  }
}