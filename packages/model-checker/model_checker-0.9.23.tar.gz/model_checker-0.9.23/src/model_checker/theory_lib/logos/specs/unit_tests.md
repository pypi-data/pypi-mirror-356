# Unit Test Completion Plan for Logos Theory

## Current Status

**Progress**: 53 ’ 49 failing unit tests (4 tests fixed)
**All 129 example tests**:  PASSING
**Core functionality**:  WORKING

## Remaining Test Failures (49 total)

### Files to Fix

1. **test_model_structure.py** - 22 failures
2. **test_operators.py** - 6 failures  
3. **test_proposition.py** - Some remaining issues
4. **test_semantic_methods.py** - Some remaining issues
5. **test_error_conditions.py** - Some remaining issues

## Systematic Fix Plan

### Phase 1: Complete test_model_structure.py (22 failures)

**Issue Pattern**: Tests likely use incorrect LogosModelStructure creation patterns

**Expected Root Causes**:
- Using `LogosModelStructure(semantics)` instead of `LogosModelStructure(model_constraints, settings)`
- Missing proper Syntax object creation
- Incorrect ModelConstraints constructor calls
- Wrong fixture usage patterns

**Fix Strategy**:
1. Apply same Syntax constructor pattern: `Syntax(['formula'], [], theory['operators'])`
2. Fix ModelConstraints calls: `ModelConstraints(settings, syntax, semantics, proposition_class)`
3. Fix LogosModelStructure calls: `LogosModelStructure(model_constraints, settings)`
4. Update attribute expectations to match actual implementation

**Files to Update**:
- `src/model_checker/theory_lib/logos/tests/test_unit/test_model_structure.py`

### Phase 2: Complete test_operators.py (6 failures)

**Issue Pattern**: Tests likely have operator access and validation issues

**Expected Root Causes**:
- Incorrect operator registry usage
- Wrong operator name expectations
- Missing subtheory loading
- Incorrect operator instantiation patterns

**Fix Strategy**:
1. Use LogosOperatorRegistry properly
2. Verify operator names match actual implementation
3. Ensure proper subtheory dependency loading
4. Update operator instantiation patterns

**Files to Update**:
- `src/model_checker/theory_lib/logos/tests/test_unit/test_operators.py`

### Phase 3: Fix remaining issues in partially fixed files

**Remaining Issues**:
- Some Syntax usage still incorrect
- ModelConstraints constructor calls with wrong argument count
- Fixture reference issues

**Fix Strategy**:
1. Search for remaining `Syntax()` calls without arguments
2. Find remaining ModelConstraints calls with 5+ arguments
3. Fix any remaining circular references like `syntax.operator_collection`
4. Update attribute access patterns

**Files to Review**:
- `test_proposition.py`
- `test_semantic_methods.py` 
- `test_error_conditions.py`

## Implementation Approach

### Step-by-Step Process

1. **Analyze Current Failures**
   ```bash
   python test_theories.py --theories logos -v | grep FAILED
   ```

2. **Fix test_model_structure.py**
   - Apply established patterns from successfully fixed files
   - Use MultiEdit for systematic replacements
   - Test incrementally

3. **Fix test_operators.py**
   - Check actual operator names using registry inspection
   - Update expected operator collections
   - Fix operator instantiation patterns

4. **Clean up remaining issues**
   - Use grep/sed for systematic pattern replacement
   - Verify no circular references remain
   - Ensure consistent fixture usage

5. **Final Validation**
   ```bash
   python test_theories.py --theories logos
   ```

### Success Criteria

- **All 359 logos tests pass** (129 examples + 230 unit tests)
- **No regressions** in example functionality
- **Consistent patterns** across all unit test files
- **High-quality coverage** of actual implementation

## Technical Patterns to Apply

### 1. Syntax Creation Pattern
```python
# L Wrong
syntax = Syntax()
syntax.read("p")

#  Correct  
syntax = Syntax(['p'], [], theory['operators'])
sentence = syntax.all_sentences['p']
```

### 2. ModelConstraints Creation Pattern
```python
# L Wrong
ModelConstraints(settings, syntax, semantics, proposition_class, operators)

#  Correct
ModelConstraints(settings, syntax, semantics, proposition_class)
```

### 3. LogosModelStructure Creation Pattern
```python
# L Wrong
LogosModelStructure(semantics)

#  Correct
LogosModelStructure(model_constraints, settings)
```

### 4. LogosProposition Creation Pattern
```python
# L Wrong
LogosProposition(semantics, "p")

#  Correct
LogosProposition(sentence, model_structure)
```

## Quality Standards

### Code Quality Requirements
- **Follow CLAUDE.md philosophies**: Fail fast, explicit parameters, no silent failures
- **Consistent patterns**: All tests use same creation patterns
- **Clear data flow**: Explicit argument passing, no hidden dependencies
- **Proper fixtures**: Use provided theory fixtures correctly

### Test Quality Requirements
- **Test actual implementation**: No tests against non-existent APIs
- **Meaningful assertions**: Test real behavior, not assumptions
- **Proper error handling**: Catch expected exceptions appropriately
- **Resource efficiency**: Use minimal settings for quick tests

## Risk Management

### Potential Issues
1. **Circular dependencies** in test setup
2. **Missing operator names** in registry
3. **Incorrect fixture assumptions** about theory loading
4. **Memory/performance issues** with model creation

### Mitigation Strategies
1. **Incremental testing**: Fix and test one file at a time
2. **Pattern verification**: Check patterns work before applying broadly
3. **Fixture validation**: Verify theory fixtures provide expected components
4. **Resource limits**: Use minimal N values and short timeouts in tests

## Timeline Estimate

- **Phase 1** (test_model_structure.py): 2-3 hours
- **Phase 2** (test_operators.py): 1-2 hours  
- **Phase 3** (cleanup): 1 hour
- **Total**: 4-6 hours of focused work

## Validation Plan

### Incremental Validation
```bash
# Test specific file
python -m pytest src/model_checker/theory_lib/logos/tests/test_unit/test_model_structure.py -v

# Test all unit tests
python -m pytest src/model_checker/theory_lib/logos/tests/test_unit/ -v

# Test complete theory
python test_theories.py --theories logos
```

### Success Metrics
- **0 failing tests** in complete logos test suite
- **All 359 tests pass** consistently
- **No performance regressions** in test execution time
- **Clear, maintainable test code** following project patterns

## Dependencies

### Required Knowledge
- LogosModelStructure constructor signature
- ModelConstraints constructor signature  
- Operator registry patterns
- Theory fixture structure

### Required Tools
- sed/grep for pattern replacement
- MultiEdit for systematic updates
- pytest for incremental testing
- Theory inspection tools for validation

## Notes

This plan builds on the successful patterns established in the first 53’49 test fixes. The remaining failures follow the same systematic patterns and should be resolved using the same proven approaches.

The key insight is that unit tests were written against assumed APIs rather than actual implementation. By updating tests to match the real implementation patterns, we maintain high test coverage while ensuring tests validate actual behavior rather than incorrect assumptions.