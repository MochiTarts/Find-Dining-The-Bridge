import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleCommonCardComponent } from './article-common-card.component';

describe('ArticleCommonCardComponent', () => {
  let component: ArticleCommonCardComponent;
  let fixture: ComponentFixture<ArticleCommonCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleCommonCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleCommonCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
