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

  getCSRFToken(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

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