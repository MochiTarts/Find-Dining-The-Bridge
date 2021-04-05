import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsArticlesComponent } from './news-articles.component';

describe('NewsArticlesComponent', () => {
  let component: NewsArticlesComponent;
  let fixture: ComponentFixture<NewsArticlesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewsArticlesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewsArticlesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
