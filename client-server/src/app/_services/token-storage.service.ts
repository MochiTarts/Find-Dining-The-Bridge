import { Injectable } from '@angular/core';
import { SocialAuthService } from 'angularx-social-login';

const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';
const AUTH_KEY = 'auth-external';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {
  constructor(private socialAuth: SocialAuthService) { }

  setProvider(provider: string) {
    window.sessionStorage.removeItem(AUTH_KEY);
    if (provider){
      window.sessionStorage.setItem(AUTH_KEY, provider);
    }
  }

  getProvider() {
    return window.sessionStorage.getItem(AUTH_KEY);
  }

  signOut(): void {
    window.sessionStorage.clear();
    if (this.getProvider()){
      this.socialAuth.signOut();
      this.setProvider('');
    }
  }

  public updateTokenAndUser(token: string): void {
    this.saveToken(token);
    // decode the token to get the user object
    const token_parts = token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    //var token_expires = new Date(token_decoded.exp * 1000);
    //var username = token_decoded.username;
    token_decoded['token'] = token;
    this.saveUser(token_decoded);

  }

  public saveToken(token: string): void {
    window.sessionStorage.removeItem(TOKEN_KEY);
    window.sessionStorage.setItem(TOKEN_KEY, token);
  }

  public getToken(): string | null {
    return window.sessionStorage.getItem(TOKEN_KEY);
  }

  public saveUser(user: any): void {
    window.sessionStorage.removeItem(USER_KEY);
    window.sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  public getUser(): any {
    const user = window.sessionStorage.getItem(USER_KEY);
    if (user) {
      return JSON.parse(user);
    }

    return {};
  }
}