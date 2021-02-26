import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';
import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from '../_services/token-storage.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-board-admin',
  templateUrl: './board-user.component.html',
  styleUrls: ['./board-user.component.scss']
})
export class BoardUserComponent implements OnInit {
  content?: string;

  constructor(private router: Router, private authService: AuthService, private userService: UserService, private tokenStorage: TokenStorageService) { }

  ngOnInit(): void {
    const token = this.tokenStorage.getToken();
    if (token) {
      this.authService.verify(token).subscribe(
        data => {
          this.userService.getUserBoard().subscribe(
            data => {
              this.content = data;
              console.log(data);
            },
            err => {
              this.content = JSON.parse(err.error).message;
            }
          );
        },
        err => {
          this.content = JSON.parse(err.error).message;
        }
      );
    } else{
      this.router.navigateByUrl('/');
    }
    
  }
}