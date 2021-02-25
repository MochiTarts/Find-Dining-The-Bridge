import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from './_services/token-storage.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private role: string = 'BU';
  isLoggedIn = false;
  showROBoard = false;
  username?: string;

  constructor(private tokenStorageService: TokenStorageService) { }

  ngOnInit(): void {
    this.isLoggedIn = !!this.tokenStorageService.getToken();

    if (this.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      console.log(user)
      this.role = user.role;

      this.showROBoard = this.role == 'BU';

      this.username = user.name;
    }
  }

  logout(): void {
    this.tokenStorageService.signOut();
    window.location.reload();
  }
}
