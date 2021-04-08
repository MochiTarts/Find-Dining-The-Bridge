import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { faStar } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-article-latest-card',
  templateUrl: './article-latest-card.component.html',
  styleUrls: ['./article-latest-card.component.scss']
})
export class ArticleLatestCardComponent implements OnInit {
  @Input() article: any;

  faStar = faStar;

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
  }

  openArticle() {
    alert(this.article.id)
  }

}
