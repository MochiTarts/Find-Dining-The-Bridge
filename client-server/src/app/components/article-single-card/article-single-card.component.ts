import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-article-single-card',
  templateUrl: './article-single-card.component.html',
  styleUrls: ['./article-single-card.component.scss']
})
export class ArticleSingleCardComponent implements OnInit {
  @Input() article: any;

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
  }

}
