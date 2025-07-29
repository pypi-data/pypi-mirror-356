# New Unit Test Implementation Plan for Logos Theory

## Overview

Replace existing problematic unit tests with clean, focused tests written against the actual working API, following the systematic testing methodology established in UNIT_TESTS.md. This approach prioritizes meaningful coverage over debugging legacy test assumptions while maintaining compliance with the project's testing standards.

## Alignment with UNIT_TESTS.md

This plan strictly follows the established testing policy:

### Testing Philosophy Compliance
- **Fail Fast**: Tests expose errors clearly rather than masking them
- **Deterministic Behavior**: No fallbacks or implicit conversions  
- **Clear Data Flow**: Explicit parameter passing and error propagation
- **Root Cause Analysis**: Tests identify structural problems, not symptoms

### Test Organization Compliance
Following the exact structure specified in UNIT_TESTS.md lines 57-64:

```
test_unit/
├── test_semantic_methods.py     # Test LogosSemantics methods
├── test_operators.py            # Test operator implementations  
├── test_registry.py             # Test LogosOperatorRegistry
├── test_proposition.py          # Test LogosProposition
├── test_model_structure.py      # Test LogosModelStructure
└── test_error_conditions.py     # Test error handling
```

## Current Situation

- **68 failing unit tests** with systemic constructor/API issues
- **129 example tests passing** - proving the core implementation works
- Legacy tests written against assumed APIs rather than actual implementation
- Tests violate UNIT_TESTS.md standards by testing wrong API contracts

## Proposed Action Plan

### Phase 1: Clean Slate (Immediate)

**Remove problematic test files:**
```bash
cd /home/benjamin/Documents/Philosophy/Projects/ModelChecker/Code/src/model_checker/theory_lib/logos/tests/test_unit/

# Remove ALL failing unit test files
rm test_error_conditions.py
rm test_model_structure.py  
rm test_operators.py
rm test_proposition.py
rm test_registry.py
rm test_semantic_methods.py
```

**Keep essential infrastructure:**
- `conftest.py` (with corrected fixtures per our fixes)
- `__init__.py`

### Phase 2: Standards-Compliant Unit Tests

Implement the exact file structure specified in UNIT_TESTS.md, focusing on implementation testing rather than end-to-end testing:

#### 2.1 `test_semantic_methods.py`

**Purpose**: Test LogosSemantics methods directly (per UNIT_TESTS.md line 59)
**Scope**: Test semantic methods without full model checking pipeline

```python
"""
Unit tests for LogosSemantics methods.

Tests validate individual semantic methods work correctly without
running the full model checking pipeline.
"""

class TestLogosSemanticInstantiation:
    """Test LogosSemantics instantiation and basic functionality."""
    
    def test_semantics_creation_valid_settings(self, basic_settings):
        """Test semantics creation with complete valid settings."""
        
    def test_semantics_missing_required_settings(self):
        """Test semantics fails with missing required settings."""
        
    def test_semantics_invalid_settings(self):
        """Test semantics fails with invalid setting values."""

class TestSemanticPrimitives:
    """Test Z3 semantic primitive creation."""
    
    def test_verify_falsify_functions(self, basic_settings):
        """Test verify and falsify function creation."""
        
    def test_possible_function(self, basic_settings):
        """Test possible state function creation."""
        
    def test_main_world_creation(self, basic_settings):
        """Test main world and main point creation."""

class TestSemanticOperations:
    """Test inherited semantic operations."""
    
    def test_fusion_operation(self, basic_settings):
        """Test state fusion operations."""
        
    def test_parthood_operations(self, basic_settings):
        """Test part-hood relationship operations."""
        
    def test_compatibility_operations(self, basic_settings):
        """Test state compatibility operations."""

class TestFrameConstraints:
    """Test frame constraint generation."""
    
    def test_frame_constraints_generation(self, basic_settings):
        """Test that frame constraints are properly generated."""
        
    def test_frame_constraints_structure(self, basic_settings):
        """Test frame constraints have expected structure."""
```

#### 2.2 `test_operators.py`

**Purpose**: Test operator implementations and semantic clauses (per UNIT_TESTS.md line 60)
**Scope**: Test individual operators without full model checking

```python
"""
Unit tests for operator implementations.

Tests validate individual operator implementations and their
semantic clauses work correctly.
"""

class TestExtensionalOperators:
    """Test extensional operator implementations."""
    
    def test_extensional_operators_available(self, extensional_theory):
        """Test all extensional operators are available."""
        
    def test_operator_properties(self, extensional_theory):
        """Test operator arity, names, and basic properties."""
        
    def test_negation_operator(self, extensional_theory):
        """Test negation operator implementation."""
        
    def test_binary_operators(self, extensional_theory):
        """Test binary operator implementations."""

class TestModalOperators:
    """Test modal operator implementations."""
    
    def test_modal_operators_available(self, modal_theory):
        """Test modal operators are correctly loaded."""
        
    def test_necessity_operator(self, modal_theory):
        """Test necessity operator implementation."""
        
    def test_possibility_operator(self, modal_theory):
        """Test possibility operator implementation."""

class TestOperatorSemanticClauses:
    """Test operator semantic clause implementations."""
    
    def test_semantic_clause_structure(self, logos_theory):
        """Test semantic clauses have proper structure."""
        
    def test_semantic_clause_execution(self, logos_theory, basic_settings):
        """Test semantic clauses can be executed."""
```

#### 2.3 `test_registry.py`

**Purpose**: Test LogosOperatorRegistry (per UNIT_TESTS.md line 61)
**Scope**: Test registry and loading mechanisms

```python
"""
Unit tests for LogosOperatorRegistry functionality.

Tests validate the operator registry system works correctly
for loading and managing operators from different subtheories.
"""

class TestRegistryBasics:
    """Test basic registry functionality."""
    
    def test_registry_creation(self):
        """Test empty registry instantiation."""
        
    def test_registry_initial_state(self):
        """Test registry initial state is correct."""

class TestSubtheoryLoading:
    """Test subtheory loading functionality."""
    
    def test_load_single_subtheory(self):
        """Test loading individual subtheories."""
        
    def test_load_multiple_subtheories(self):
        """Test loading multiple subtheories."""
        
    def test_incremental_loading(self):
        """Test loading subtheories incrementally."""

class TestDependencyResolution:
    """Test dependency resolution functionality."""
    
    def test_automatic_dependency_resolution(self):
        """Test dependencies are automatically resolved."""
        
    def test_dependency_chain_resolution(self):
        """Test complex dependency chains are resolved."""

class TestOperatorAccess:
    """Test operator access functionality."""
    
    def test_operator_retrieval(self):
        """Test accessing loaded operators."""
        
    def test_operator_collection_structure(self):
        """Test operator collection has expected structure."""

class TestErrorHandling:
    """Test registry error handling."""
    
    def test_invalid_subtheory_handling(self):
        """Test graceful handling of invalid subtheory names."""
        
    def test_empty_subtheory_list(self):
        """Test handling of empty subtheory lists."""
```

#### 2.4 `test_proposition.py`

**Purpose**: Test LogosProposition (per UNIT_TESTS.md line 62)
**Scope**: Test proposition class methods and integration

```python
"""
Unit tests for LogosProposition functionality.

Tests validate the LogosProposition class and its methods
work correctly in isolation and integration.
"""

class TestPropositionCreation:
    """Test LogosProposition instantiation."""
    
    def test_proposition_creation_valid_args(self, logos_theory, basic_settings):
        """Test proposition creation with proper arguments."""
        
    def test_proposition_creation_invalid_args(self):
        """Test proposition creation fails with invalid arguments."""
        
    def test_proposition_attributes(self, logos_theory, basic_settings):
        """Test proposition has expected attributes."""

class TestPropositionConstraints:
    """Test proposition constraint generation."""
    
    def test_proposition_constraints_method(self, logos_theory, basic_settings):
        """Test static proposition_constraints method."""
        
    def test_constraint_generation_structure(self, logos_theory, basic_settings):
        """Test generated constraints have proper structure."""

class TestPropositionIntegration:
    """Test proposition integration with other components."""
    
    def test_proposition_model_integration(self, logos_theory, basic_settings):
        """Test integration with model structures."""
        
    def test_proposition_sentence_integration(self, logos_theory, basic_settings):
        """Test integration with sentence objects."""

class TestPropositionUtilities:
    """Test proposition utility methods."""
    
    def test_proposition_string_representation(self, logos_theory, basic_settings):
        """Test proposition string representation."""
        
    def test_proposition_equality(self, logos_theory, basic_settings):
        """Test proposition equality and hashing."""
```

#### 2.5 `test_model_structure.py`

**Purpose**: Test LogosModelStructure (per UNIT_TESTS.md line 63)
**Scope**: Test model structure class and its methods

```python
"""
Unit tests for LogosModelStructure functionality.

Tests validate the LogosModelStructure class and its methods
work correctly in isolation.
"""

class TestModelStructureCreation:
    """Test LogosModelStructure instantiation."""
    
    def test_model_structure_creation(self, logos_theory, basic_settings):
        """Test model structure creation with valid arguments."""
        
    def test_model_structure_invalid_args(self):
        """Test model structure creation fails with invalid arguments."""

class TestModelConstraintIntegration:
    """Test integration with ModelConstraints."""
    
    def test_model_constraints_integration(self, logos_theory, basic_settings):
        """Test integration with ModelConstraints objects."""
        
    def test_constraint_processing(self, logos_theory, basic_settings):
        """Test constraint processing and Z3 integration."""

class TestModelValidation:
    """Test model validation methods."""
    
    def test_check_result_method(self, logos_theory, basic_settings):
        """Test check_result method functionality."""
        
    def test_model_status_attributes(self, logos_theory, basic_settings):
        """Test model status attributes are properly set."""

class TestModelUtilities:
    """Test model utility methods."""
    
    def test_model_string_representation(self, logos_theory, basic_settings):
        """Test model string representation."""
        
    def test_model_attribute_access(self, logos_theory, basic_settings):
        """Test model attribute access patterns."""
```

#### 2.6 `test_error_conditions.py`

**Purpose**: Test error handling and edge cases (per UNIT_TESTS.md line 64)
**Scope**: Test expected failure conditions

```python
"""
Unit tests for error conditions and edge cases.

Tests validate error handling and edge cases throughout
the logos theory implementation.
"""

class TestSemanticErrorConditions:
    """Test error conditions in semantic classes."""
    
    def test_invalid_settings_handling(self):
        """Test handling of invalid settings."""
        
    def test_resource_exhaustion_scenarios(self):
        """Test behavior under resource exhaustion."""

class TestOperatorErrorConditions:
    """Test error conditions in operator handling."""
    
    def test_invalid_operator_usage(self):
        """Test handling of invalid operator combinations."""
        
    def test_missing_operator_dependencies(self):
        """Test handling of missing operator dependencies."""

class TestIntegrationErrorConditions:
    """Test error conditions in component integration."""
    
    def test_mismatched_component_integration(self):
        """Test integration between mismatched components."""
        
    def test_timeout_conditions(self):
        """Test behavior under timeout conditions."""

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_minimal_settings(self):
        """Test with minimal valid settings."""
        
    def test_extreme_parameter_values(self):
        """Test with extreme but valid parameter values."""
```

### Phase 3: Implementation Strategy

#### 3.1 Strict Standards Compliance

**Follow UNIT_TESTS.md requirements exactly:**
- **Isolation**: Each test works independently without external dependencies (line 154)
- **Fixtures**: Use pytest fixtures for common setup (line 155)  
- **Parametrization**: Use `@pytest.mark.parametrize` for testing multiple inputs (line 156)
- **Error Testing**: Include tests for expected failure conditions (line 157)
- **Coverage**: Aim for comprehensive coverage of public API methods (line 158)

#### 3.2 Use Working API Patterns

**Base all tests on successful example patterns:**
- Use actual constructor signatures from passing examples
- Use working fixture patterns from `conftest.py`
- Test actual attributes and methods that exist in implementation
- Use `logos.get_theory()` pattern that works

#### 3.3 Testing Philosophy Implementation

**Follow CLAUDE.md and UNIT_TESTS.md philosophies:**
- **Fail Fast**: Let errors occur naturally, test clear error messages
- **Explicit Parameters**: Test that required parameters are actually required
- **No Defensive Programming**: Don't test fallbacks or implicit conversions
- **Root Cause Testing**: Test structural problems, not symptoms

#### 3.4 CLI Integration Compliance

**Ensure compatibility with test_theories.py CLI:**
- Support `python test_theories.py --theories logos --package` (unit tests only)
- Support specific unit test categories: `--semantics`, `--operators`, `--registry`, etc.
- Integrate with inclusive-by-default CLI design
- Provide consistent output format

### Phase 4: Quality Standards

#### 4.1 Test Quality Requirements (per UNIT_TESTS.md)

- **Test real behavior**: Test actual implementation, not assumptions
- **Meaningful assertions**: Test functionality, not just existence
- **Clear test names**: Describe specific behavior being tested
- **Minimal test data**: Use smallest examples that test the behavior
- **Fast execution**: Unit tests should complete quickly for rapid feedback

#### 4.2 Coverage Goals (per UNIT_TESTS.md lines 220-224)

**Required Coverage:**
- **Unit Tests**: Must test all public methods of core classes
- **Error Tests**: Must test expected failure modes  
- **Integration Tests**: Must test component interactions (within unit scope)

**Performance Requirements:**
- **Test Timeouts**: Use reasonable timeouts
- **Resource Limits**: Set appropriate N values  
- **Fast Unit Tests**: Complete quickly for rapid feedback

### Phase 5: Success Criteria

#### 5.1 Compliance Validation

- **0 failing unit tests** after implementation
- **Full CLI integration** with test_theories.py
- **Standards compliance** with UNIT_TESTS.md requirements
- **Fixture compatibility** with existing conftest.py

#### 5.2 Quality Measures

- **Testing Philosophy Alignment**: All tests follow fail-fast, explicit principles
- **API Coverage**: All public methods of core classes tested
- **Error Coverage**: All expected failure modes tested
- **Integration Coverage**: Component interactions tested (within unit scope)

## Implementation Timeline

### Immediate (This Session)
- Remove failing unit test files per Phase 1
- Validate conftest.py fixtures are properly configured

### Short-term (Next Session)  
- Implement `test_semantic_methods.py` following exact UNIT_TESTS.md specifications
- Verify CLI integration works with `--package --semantics`
- Validate all tests pass and provide meaningful coverage

### Medium-term (Follow-up Sessions)
- Implement remaining test files in specified order
- Ensure each file fully complies with UNIT_TESTS.md standards
- Validate complete CLI integration and performance requirements

## Benefits of Standards-Compliant Approach

### Technical Benefits
- **Full compliance** with established testing policy
- **CLI integration** that works with existing project infrastructure  
- **Standards-based** test organization and execution
- **Performance compliant** with project requirements

### Process Benefits
- **Consistent with project methodology** established in UNIT_TESTS.md
- **Extensible to other theories** using same standardized approach
- **Maintainable** through consistent patterns and organization
- **Quality assured** through established quality requirements

## Risk Mitigation

### Compliance Risks
- **Standards drift**: Regular validation against UNIT_TESTS.md
- **CLI integration issues**: Test with full test_theories.py command set
- **Performance issues**: Monitor test execution times

### Technical Risks  
- **API changes**: Base tests on stable, working example patterns
- **Fixture issues**: Validate conftest.py compatibility
- **Coverage gaps**: Follow systematic coverage requirements from UNIT_TESTS.md

## Conclusion

This standards-compliant approach ensures new unit tests fully align with the established testing methodology in UNIT_TESTS.md while providing the working, valuable tests needed to replace the problematic legacy tests. By following the exact specifications for file organization, testing philosophy, and quality requirements, we create a robust foundation that supports the logos theory's role in the broader ModelChecker testing strategy.