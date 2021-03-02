import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TokenStorageService } from './token-storage.service';

//const AUTH_API = 'http://localhost:8000/api/auth/';
const AUTH_API = '/api/auth/';
//const AUTH_API = '/auth/'
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient, private tokenStorage: TokenStorageService,) { }

  // email can be used as alternative to username (backend accepts both)
  login(username: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'signin/', JSON.stringify({
      username,
      password
    }), httpOptions);
  }

  register(username: string, email: string, password: string, role: string): Observable<any> {

    return this.http.post(AUTH_API + 'signup/', JSON.stringify({
      username,
      email,
      password,
      role,
    }), httpOptions);
  }

  verify(token: string): Observable<any> {
    return this.http.post(AUTH_API + 'verify/', JSON.stringify({
      token,
    }), httpOptions);
  }

  
  refreshToken(): Observable<any> {
    var refreshToken = this.tokenStorage.getRefreshToken();
    return this.http.post(AUTH_API + 'refresh/', JSON.stringify({
      'refresh': refreshToken,
    }), httpOptions);
  }
  
}