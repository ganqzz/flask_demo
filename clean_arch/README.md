# Python Clean Architecture Example

- DI
- Onion Architecture
- Controller(Web) -- UseCase -- Domain
  Repository(DB) --/

- Repository/UseCase(及びInteractor)については、個々のアクション毎あるいは更新/参照系毎に分割することも考えられる。

- Testing
    * using Mock

- TODO:
    infrastructure/persistence/repository/implementation
    interfaceはdomain側に
