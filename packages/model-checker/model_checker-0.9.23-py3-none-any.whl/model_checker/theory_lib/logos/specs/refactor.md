# Logos Theory Refactor Plan

## Executive Summary

The logos theory implementation has fundamental issues preventing successful execution of unit tests. While the test infrastructure refactor completed successfully (129 examples from 5 subtheories are properly discoverable via `test_theories.py --theories logos -v`), the underlying semantic implementation has critical bugs that need systematic resolution.

## Current Status

###  Working Components
- **Test Infrastructure**: Successfully refactored with unified `examples.py` and `test_logos_examples.py`
- **Operator Registry System**: `LogosOperatorRegistry` properly loads subtheory operators
- **Example Organization**: 129 examples properly categorized and prefixed across 5 subtheories
- **Test Discovery**: `test_theories.py` correctly finds and attempts to run all logos tests

### L Critical Issues Identified

1. **Z3 Type Coercion Failures** (Primary Issue)
   - Error: `z3.z3types.Z3Exception: Python value cannot be used as a Z3 integer`
   - Location: `model.py:212` in `fusion()` method: `return bit_s | bit_t`
   - Root Cause: Attempting bitwise OR on incompatible Z3 types

2. **Semantic Framework Integration Problems**
   - Inconsistent inheritance from base model classes
   - Missing or incorrect type conversions in truthmaker semantics
   - Potential issues with state representation and world calculations

3. **Operator Implementation Gaps**
   - Some operators may not have proper semantic clause implementations
   - Potential conflicts between operators from different subtheories
   - Missing operator type definitions causing parsing errors

## Detailed Error Analysis

### Primary Error Stack Trace
```
File "semantic.py", line 87: self.true_at(premise, self.main_point)
File "semantic.py", line 139: Exists(x, z3.And(self.is_part_of(x, eval_world), self.verify(x, sentence_letter)))
File "model.py", line 281: self.fusion(bit_s, bit_t) == bit_t
File "model.py", line 212: return bit_s | bit_t
z3.z3types.Z3Exception: Python value cannot be used as a Z3 integer
```

### Error Propagation Pattern
1. **Test Execution**: `run_test()` calls `ModelConstraints()`
2. **Model Creation**: Creates `LogosSemantics` instance
3. **Premise Processing**: Calls `premise_behavior(premise)`
4. **Truth Evaluation**: Calls `true_at(premise, self.main_point)`
5. **State Operations**: Calls `is_part_of()` which uses `fusion()`
6. **Z3 Failure**: Bitwise OR operation fails on incompatible types

## Refactor Plan

### Phase 1: Critical Bug Fixes (Priority: URGENT)

#### 1.1 Fix Z3 Type Coercion in Fusion Operation
**File**: `src/model_checker/theory_lib/logos/semantic.py`

**Problem**: The inherited `fusion()` method from `SemanticDefaults` is receiving incompatible Z3 types.

**Solution**:
```python
def fusion(self, bit_s, bit_t):
    """
    Logos-specific fusion operation with proper type handling.
    
    Ensures both operands are properly converted to Z3 BitVec types
    before performing bitwise OR operation.
    """
    # Ensure both operands are Z3 BitVec with same bit-width
    if not isinstance(bit_s, z3.BitVecRef):
        if isinstance(bit_s, int):
            bit_s = z3.BitVecVal(bit_s, self.N)
        else:
            raise TypeError(f"Cannot convert {type(bit_s)} to BitVec")
    
    if not isinstance(bit_t, z3.BitVecRef):
        if isinstance(bit_t, int):
            bit_t = z3.BitVecVal(bit_t, self.N)
        else:
            raise TypeError(f"Cannot convert {type(bit_t)} to BitVec")
    
    # Ensure same bit-width
    if bit_s.size() != bit_t.size():
        target_size = max(bit_s.size(), bit_t.size())
        bit_s = z3.ZeroExt(target_size - bit_s.size(), bit_s)
        bit_t = z3.ZeroExt(target_size - bit_t.size(), bit_t)
    
    return bit_s | bit_t
```

#### 1.2 Fix State Representation Issues
**File**: `src/model_checker/theory_lib/logos/semantic.py`

**Problem**: Inconsistent state representation between worlds and state operations.

**Investigation Required**:
- Check `self.main_point` initialization and type
- Verify world representation consistency
- Ensure proper bit-vector sizing throughout

**Action Items**:
1. Add type checking in `__init__()` method
2. Ensure `self.main_point` is proper Z3 BitVec
3. Add validation for all state-related operations

#### 1.3 Fix Truth Evaluation Method
**File**: `src/model_checker/theory_lib/logos/semantic.py`, line 139

**Problem**: Truth evaluation is calling operations on incompatible types.

**Solution**:
```python
def true_at(self, sentence_letter, eval_world):
    """
    Enhanced truth evaluation with type safety.
    """
    # Ensure eval_world is proper Z3 BitVec
    if not isinstance(eval_world, z3.BitVecRef):
        if isinstance(eval_world, int):
            eval_world = z3.BitVecVal(eval_world, self.N)
        else:
            raise TypeError(f"eval_world must be BitVec, got {type(eval_world)}")
    
    x = z3.BitVec(f'state_{sentence_letter}_{id(eval_world)}', self.N)
    return z3.Exists(x, z3.And(
        self.is_part_of(x, eval_world), 
        self.verify(x, sentence_letter)
    ))
```

### Phase 2: Semantic Framework Stabilization (Priority: HIGH)

#### 2.1 Standardize Type System
**Files**: All semantic and operator files

**Objectives**:
- Establish consistent Z3 type usage across all operations
- Create type validation utilities
- Add comprehensive type checking

**Implementation**:
```python
class LogosTypeSystem:
    """Type safety utilities for logos semantic operations."""
    
    @staticmethod
    def ensure_bitvec(value, bit_width):
        """Ensure value is Z3 BitVec with specified width."""
        if isinstance(value, z3.BitVecRef):
            if value.size() != bit_width:
                if value.size() < bit_width:
                    return z3.ZeroExt(bit_width - value.size(), value)
                else:
                    return z3.Extract(bit_width - 1, 0, value)
            return value
        elif isinstance(value, int):
            return z3.BitVecVal(value, bit_width)
        else:
            raise TypeError(f"Cannot convert {type(value)} to BitVec({bit_width})")
    
    @staticmethod
    def validate_state_operation(bit_s, bit_t, operation_name):
        """Validate state operation inputs."""
        if not isinstance(bit_s, z3.BitVecRef):
            raise TypeError(f"{operation_name}: bit_s must be BitVec, got {type(bit_s)}")
        if not isinstance(bit_t, z3.BitVecRef):
            raise TypeError(f"{operation_name}: bit_t must be BitVec, got {type(bit_t)}")
        if bit_s.size() != bit_t.size():
            raise ValueError(f"{operation_name}: BitVec size mismatch: {bit_s.size()} != {bit_t.size()}")
```

#### 2.2 Audit and Fix Operator Implementations
**Files**: All `subtheories/*/operators.py`

**Audit Checklist**:
- [ ] All operators have proper semantic clauses
- [ ] Semantic clauses use consistent type system
- [ ] No undefined operators referenced in examples
- [ ] Operator precedence properly defined
- [ ] All subtheory dependencies correctly loaded

**Action Plan**:
1. Create operator validation script
2. Test each operator in isolation
3. Fix missing or broken semantic implementations
4. Ensure proper integration between subtheories

### Phase 3: Example and Test Validation (Priority: MEDIUM)

#### 3.1 Example Validation
**Files**: All `subtheories/*/examples.py`

**Validation Tasks**:
- Check all example settings are valid
- Ensure all referenced operators exist
- Validate formula syntax
- Verify expectation settings are correct

#### 3.2 Progressive Testing Strategy
**Implementation**:
1. Create minimal test examples for each subtheory
2. Test subtheories in isolation first
3. Test subtheory combinations
4. Run full test suite

**Test Hierarchy**:
```python
# Minimal examples for validation
minimal_examples = {
    'extensional': ['A', ['A'], {'N': 2, 'expectation': False}],
    'modal': ['\\Box A', ['A'], {'N': 3, 'expectation': False}],
    'constitutive': ['A \\equiv A', [], {'N': 2, 'expectation': False}],
    'counterfactual': ['A \\boxright A', [], {'N': 2, 'expectation': False}],
    'relevance': ['A \\preceq A', [], {'N': 2, 'expectation': False}],
}
```

### Phase 4: Documentation and Testing Infrastructure (Priority: LOW)

#### 4.1 Enhanced Error Diagnostics
**File**: `src/model_checker/theory_lib/logos/diagnostic.py` (new)

**Features**:
- Detailed error reporting for type mismatches
- State operation debugging utilities
- Operator validation tools
- Example syntax checking

#### 4.2 Development Testing Tools
**File**: `src/model_checker/theory_lib/logos/dev_tools.py` (new)

**Tools**:
- Individual operator testing
- Type system validation
- Semantic framework debugging
- Example generation utilities

## Implementation Timeline

### Week 1: Emergency Fixes
- [ ] Fix Z3 type coercion in fusion operation
- [ ] Implement type safety in truth evaluation
- [ ] Create basic type validation utilities
- [ ] Test with minimal examples

### Week 2: Systematic Validation
- [ ] Audit all operator implementations
- [ ] Fix missing semantic clauses
- [ ] Validate all examples
- [ ] Test subtheories in isolation

### Week 3: Integration Testing
- [ ] Test subtheory combinations
- [ ] Run progressive test suite
- [ ] Fix integration issues
- [ ] Validate full example set

### Week 4: Documentation and Tools
- [ ] Create diagnostic utilities
- [ ] Document type system
- [ ] Create development tools
- [ ] Final validation and testing

## Risk Assessment

### High Risk
- **Z3 Type System**: Core issue affecting all operations
- **Semantic Framework**: Fundamental changes may break existing functionality
- **Operator Dependencies**: Changes may cascade across subtheories

### Medium Risk
- **Example Validation**: Many examples may need settings adjustments
- **Performance**: Type checking may impact execution speed
- **Compatibility**: Changes may affect integration with other theories

### Low Risk
- **Documentation**: Improvements won't affect functionality
- **Development Tools**: Additive enhancements only
- **Test Infrastructure**: Already working correctly

## Success Criteria

### Phase 1 Success
- [ ] All minimal examples execute without Z3 errors
- [ ] Basic extensional operators work correctly
- [ ] Type system validation passes

### Phase 2 Success
- [ ] All subtheory examples run individually
- [ ] No operator implementation gaps
- [ ] Cross-subtheory integration works

### Phase 3 Success
- [ ] `test_theories.py --theories logos -v` shows >90% pass rate
- [ ] All 129 examples execute (may not all pass expectation, but no errors)
- [ ] Performance acceptable for practical use

### Final Success
- [ ] Logos theory fully functional and reliable
- [ ] Comprehensive test coverage
- [ ] Clear documentation and development tools
- [ ] Ready for production use

## Notes

1. **Preserve Test Infrastructure**: The current test refactor is working correctly and should not be modified during this semantic refactor.

2. **Incremental Approach**: Fix the most critical issues first (Z3 types) before tackling broader semantic problems.

3. **Backward Compatibility**: Ensure changes don't break the working subtheory structure.

4. **Documentation**: Document all type system decisions and semantic framework changes for future maintainers.

5. **Testing Strategy**: Use minimal examples for early validation before testing the full 129-example suite.

This refactor plan addresses the core issues preventing logos theory functionality while maintaining the successful test infrastructure already implemented.