describe('Home Page', function() {
    it('successfully loads', function() {
      cy.visit('http://localhost:8080') // replace with your app's url
    })
  })

  describe('Book Ordering Process', function() {
    it('orders a book', function() {
      cy.visit('http://localhost:8080')
  
      // Go to Books
      cy.get('.btn.btn-outline-success').first().click()

      // Go to first book
      cy.get('.btn.btn-outline-success.btn-lg').first().click()

      // Add the book to the cart
      cy.get('.btn.btn-outline-success.btn-lg').click()
  
      // Select Country
      cy.get('#country').select('Estonia')

      // Submit Order
      cy.contains('Submit').click()

      // Check that we've been redirected to the confirmation page
      cy.url().should('include', '/checkout/1/confirmation')

      // Check that the confirmation message is displayed
      cy.contains('Status: Order Approved')

      // Check that at least one suggested book is displayed
      cy.contains('Suggested Books')
      cy.contains('Book ID:')
      cy.contains('Author:')
    })
  })