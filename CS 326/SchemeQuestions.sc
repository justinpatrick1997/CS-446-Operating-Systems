;Justin Patrick
;9/27/18
;CS 326

;Question 1(a)
(define (is-unique? num L)
(if (null? L)
#t
(if (= num (car L))
#f
(is-unique? num (cdr L)))))
(define (is-set? L)
(if (null? L)
#t
(if (is-unique? (car L) (cdr L))
(is-set? (cdr L))
#f)))


;Question 1(b)
(define (make-set L)
(fold-right (lambda (f r)
(cons f (filter (lambda (x) (not (equal? x f))) r))) '() L))

;Question 1(c)
(define (subsets L)
(if (null ? L)
(list ())
(extend (subsets (cdr L))
(foo L))


;Question 1(d)
(define (union a b)
(cond ((null? b) a)
    ((member (car b) a)
    (union a (cdr b)))
    (else (union (cons (car b) a) (cdr b)))))


;Question 1(e)
(define (intersection a b)
  (if (null? a)
      '()
  (if (contains (car a) b)
      (cons (car a) (intersection (cdr a) b))
      (intersection (cdr a) b))))
(define contains member)


;Question 2(a)
(define (Val T)
(List-ref T 0)
)
(define (left T)
(List-ref T 1)
)
define (right T)
(List-ref T 2)
)

(define (tree-member? 17 T)
(if (V(equal?(node T))
#t
else
)



;Question 2(b)
(define (Val T)
(List-ref T 0)
)
(define (left T)
(List-ref T 1)
)
define (right T)
(List-ref T 2)
)

(define(preorder L))
(cond[equal?(length L)0())
(list(val L)))
(else(append(preorder(left L))(preorder(right L))))


;Question 2(c)
(define (Val T)
(List-ref T 0)
)
(define (left T)
(List-ref T 1)
)
define (right T)
(List-ref T 2)
)

(define(inorder L))
(list(val L)))
else(append(inorder(left L))
    (cond[equal?(length L)0()]
    append(preorder(right L)))]


;Question 3(a)
(define (del V L)
  (cond ((null? L) L)
      ((list? (car L))
      (cons (del V (car L)) (del V (cdr L))))
      ((equal? V (car L)) (del V (cdr L)))
      (else (cons (car L) (del V (cdr L))))))


;Question 4(a)
(define-structure
(node
  (constructor make-node (ben #!optional left right)))
  ben(left'())(right'()))

(define (insert-bst V T)
(if (null? T)
  (make-node V)
  (let ((ben (node-ben T)))
(cond ((< x ben)
  (make-node ben
  (insert-bst V (node-left T))
  (node-right T)))
  ((> V ben)
  (make-node ben
  (node-left T)
  (insert-bst V (node-right T))))
  (else T)))))
