from SolidityParser import SolidityParser
from gen.SolidityVisitor import SolidityVisitor
from gen.SolidityLexer import SolidityLexer
from antlr4 import *
from sol2DIR.Variable import *
from collections import defaultdict, OrderedDict, deque
import re


class DystonizerBase(SolidityVisitor):

    def getResult(self, ctx: ParserRuleContext):
        res = ''
        try:
            for child in ctx.children:
                res += self.visit(child)
        # ctx가 terminal node일 때
        except AttributeError:
            res += self.visit(ctx)
        # ctx가 children이 없을 때
        except TypeError:
            pass
        return res

    # Visit a parse tree produced by SolidityParser#terminalNode.
    def visitTerminal(self, node):
        return node.symbol.text

    # Visit a parse tree produced by SolidityParser#sourceUnit.
    def visitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        res = self.getResult(ctx).replace('<EOF>', '')
        print(res)
        return res

    # Visit a parse tree produced by SolidityParser#pragmaDirective.
    def visitPragmaDirective(self, ctx: SolidityParser.PragmaDirectiveContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#VersionPragma.
    def visitVersionPragma(self, ctx: SolidityParser.VersionPragmaContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#version.
    def visitVersion(self, ctx: SolidityParser.VersionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#versionOperator.
    def visitVersionOperator(self, ctx: SolidityParser.VersionOperatorContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#versionConstraint.
    def visitVersionConstraint(self, ctx: SolidityParser.VersionConstraintContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#contractDefinition.
    def visitContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#contractPart.
    def visitContractPart(self, ctx: SolidityParser.ContractPartContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#stateVariableDeclaration.
    def visitStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx: SolidityParser.ConstructorDefinitionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#functionDefinition.
    def visitFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#returnParameters.
    def visitReturnParameters(self, ctx: SolidityParser.ReturnParametersContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#modifierList.
    def visitModifierList(self, ctx: SolidityParser.ModifierListContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#modifier.
    def visitModifier(self, ctx: SolidityParser.ModifierContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#parameterList.
    def visitParameterList(self, ctx: SolidityParser.ParameterListContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#parameter.
    def visitParameter(self, ctx: SolidityParser.ParameterContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#enumValue.
    def visitEnumValue(self, ctx: SolidityParser.EnumValueContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#enumDefinition.
    def visitEnumDefinition(self, ctx: SolidityParser.EnumDefinitionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx: SolidityParser.VariableDeclarationContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#typeName.
    def visitTypeName(self, ctx: SolidityParser.TypeNameContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#userDefinedTypeName.
    def visitUserDefinedTypeName(self, ctx: SolidityParser.UserDefinedTypeNameContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#mapping.
    def visitMapping(self, ctx: SolidityParser.MappingContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#stateMutability.
    def visitStateMutability(self, ctx: SolidityParser.StateMutabilityContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#block.
    def visitBlock(self, ctx: SolidityParser.BlockContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#statement.
    def visitStatement(self, ctx: SolidityParser.StatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#expressionStatement.
    def visitExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#ifStatement.
    def visitIfStatement(self, ctx: SolidityParser.IfStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#whileStatement.
    def visitWhileStatement(self, ctx: SolidityParser.WhileStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#simpleStatement.
    def visitSimpleStatement(self, ctx: SolidityParser.SimpleStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#forStatement.
    def visitForStatement(self, ctx: SolidityParser.ForStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx: SolidityParser.DoWhileStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#continueStatement.
    def visitContinueStatement(self, ctx: SolidityParser.ContinueStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#breakStatement.
    def visitBreakStatement(self, ctx: SolidityParser.BreakStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#returnStatement.
    def visitReturnStatement(self, ctx: SolidityParser.ReturnStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#variableDeclarationStatement.
    def visitVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#elementaryTypeName.
    def visitElementaryTypeName(self, ctx: SolidityParser.ElementaryTypeNameContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#AndExpr.
    def visitAndExpr(self, ctx: SolidityParser.AndExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#ParenthesisExpr.
    def visitParenthesisExpr(self, ctx: SolidityParser.ParenthesisExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx: SolidityParser.BitwiseOrExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#AllExpr.
    def visitAllExpr(self, ctx: SolidityParser.AllExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#IteExpr.
    def visitIteExpr(self, ctx: SolidityParser.IteExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#PowExpr.
    def visitPowExpr(self, ctx: SolidityParser.PowExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#StringLiteralExpr.
    def visitStringLiteralExpr(self, ctx: SolidityParser.StringLiteralExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#PlusMinusExpr.
    def visitPlusMinusExpr(self, ctx: SolidityParser.PlusMinusExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#CompExpr.
    def visitCompExpr(self, ctx: SolidityParser.CompExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#IndexExpr.
    def visitIndexExpr(self, ctx: SolidityParser.IndexExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#SignExpr.
    def visitSignExpr(self, ctx: SolidityParser.SignExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#NumberLiteralExpr.
    def visitNumberLiteralExpr(self, ctx: SolidityParser.NumberLiteralExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx: SolidityParser.BitwiseNotExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx: SolidityParser.IdentifierExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BooleanLiteralExpr.
    def visitBooleanLiteralExpr(self, ctx: SolidityParser.BooleanLiteralExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#MeExpr.
    def visitMeExpr(self, ctx: SolidityParser.MeExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#NotExpr.
    def visitNotExpr(self, ctx: SolidityParser.NotExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BitShiftExpr.
    def visitBitShiftExpr(self, ctx: SolidityParser.BitShiftExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx: SolidityParser.BitwiseAndExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#MultDivModExpr.
    def visitMultDivModExpr(self, ctx: SolidityParser.MultDivModExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#AssignmentExpr.
    def visitAssignmentExpr(self, ctx: SolidityParser.AssignmentExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#TupleExpr.
    def visitTupleExpr(self, ctx: SolidityParser.TupleExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#OrExpr.
    def visitOrExpr(self, ctx: SolidityParser.OrExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx: SolidityParser.FunctionCallExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#EqExpr.
    def visitEqExpr(self, ctx: SolidityParser.EqExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#PostCrementExpr.
    def visitPostCrementExpr(self, ctx: SolidityParser.PostCrementExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#PrimitiveCastExpr.
    def visitPrimitiveCastExpr(self, ctx: SolidityParser.PrimitiveCastExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#BitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx: SolidityParser.BitwiseXorExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx: SolidityParser.MemberAccessExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#PreCrementExpr.
    def visitPreCrementExpr(self, ctx: SolidityParser.PreCrementExprContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#functionCallArguments.
    def visitFunctionCallArguments(self, ctx: SolidityParser.FunctionCallArgumentsContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#tupleExpression.
    def visitTupleExpression(self, ctx: SolidityParser.TupleExpressionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#elementaryTypeNameExpression.
    def visitElementaryTypeNameExpression(self, ctx: SolidityParser.ElementaryTypeNameExpressionContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#numberLiteral.
    def visitNumberLiteral(self, ctx: SolidityParser.NumberLiteralContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#annotatedTypeName.
    def visitAnnotatedTypeName(self, ctx: SolidityParser.AnnotatedTypeNameContext):
        return self.getResult(ctx)

    # Visit a parse tree produced by SolidityParser#identifier.
    def visitIdentifier(self, ctx: SolidityParser.IdentifierContext):
        return self.getResult(ctx)


class DystoneizerFormatter(DystonizerBase):

    def __init__(self):
        self.tail = defaultdict(lambda: ' ')
        self.tail.update(dict.fromkeys(['{', '}', ';'], '\n'))
        self.tail.update(dict.fromkeys(['^'], ''))
        self.head = defaultdict(lambda: '')
        self.tap_cnt = 0
        self.TAP = '\t'

    def getTapStr(self):
        return self.TAP * self.tap_cnt

    # 삽입할 탭의 개수를 1개 증가 또는 감소시킴
    def adjustTapCnt(self, txt):
        if txt == '{':
            self.tap_cnt += 1
        elif txt == '}':
            self.tap_cnt -= 1
        self.head['}'] = self.getTapStr()

    # 가독성 좋게 띄어쓰기를 줄임
    def removeRedundantSpace(self, res):
        res = re.sub(' ;', ';', res)
        res = re.sub(' [(] ', '(', res)
        res = re.sub(' [)]', ')', res)
        res = re.sub(' [\[] ', '[', res)
        res = re.sub(' ]', ']', res)
        res = re.sub(' ,', ',', res)
        res = re.sub('[+]', '+ ', res)
        return res

    def visitTerminal(self, node):
        txt = node.symbol.text
        self.adjustTapCnt(txt)
        return self.head[txt] + txt + self.tail[txt]

    def visitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        res = self.removeRedundantSpace(self.getResult(ctx).replace('<EOF>', ''))
        with open('output/dystone_output.stn', 'w') as f:
            f.write(res)
        print(res)
        return res

    def visitPragmaDirective(self, ctx: SolidityParser.PragmaDirectiveContext):
        return self.getResult(ctx) + '\n'

    def visitContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        res = ''
        # contract identifier {
        for i in range(3):
            res += self.getResult(ctx.getChild(i))
        # contractParts
        for i in range(3, ctx.getChildCount() - 1):
            # 만약 해당 노드의 자식 타입이 ConstructorDefinitionContext or FunctionDefinitionContext 이면 앞에 어떤 prefix를 덧붙임.
            if isinstance(ctx.getChild(i).getChild(0), SolidityParser.ConstructorDefinitionContext) or \
                    isinstance(ctx.getChild(i).getChild(0), SolidityParser.FunctionDefinitionContext):
                res += '\n'
            res += self.getTapStr() + self.getResult(ctx.getChild(i))
        # }
        res += self.getResult(ctx.getChild(ctx.getChildCount() - 1))
        return res

    def visitEnumValue(self, ctx: SolidityParser.EnumValueContext):
        res = ''
        if ctx.children:
            for child in ctx.children:
                res += self.getTapStr() + self.getResult(child)
        return res

    def visitStatement(self, ctx: SolidityParser.StatementContext):
        res = ''
        if ctx.children:
            for child in ctx.children:
                res += self.getTapStr() + self.getResult(child)
        return res


class DystonizerStep1_2(DystoneizerFormatter):

    def __init__(self):
        super(DystonizerStep1_2, self).__init__()
        self.variable_num = 1
        self.function_num = 0

    def insertFunctionNum(self):
        self.function_num += 1
        return '\n' + self.getTapStr() + '@c' + str(self.function_num) + '\n'

    def insertVariableNum(self, isAddress=False):
        self.variable_num += 1
        prefix = '!_t' if isAddress else '@_t'
        return prefix + str(self.variable_num) + ' '

    def isParentExist(self, queryCtx: ParserRuleContext, targetType) -> bool:
        # queryCtx : 현재 노드, targetType : 목표 타입
        if type(queryCtx) == targetType:
            return True
        if queryCtx.parentCtx:
            return self.isParentExist(queryCtx.parentCtx, targetType)
        return False

    def visitContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        # contractDefinition : ('contract') idf=identifier '{' parts+=contractPart* '}';
        res = ''
        # contract identifier {
        for i in range(3):
            res += self.getResult(ctx.getChild(i))
        # contractParts
        for i in range(3, ctx.getChildCount() - 1):
            # 만약 해당 노드의 자식 타입이 ConstructorDefinitionContext or FunctionDefinitionContext 이면 앞에 prefix를 덧붙임.
            if isinstance(ctx.getChild(i).getChild(0), SolidityParser.ConstructorDefinitionContext) or \
                    isinstance(ctx.getChild(i).getChild(0), SolidityParser.FunctionDefinitionContext):
                res += self.insertFunctionNum()
            res += self.getTapStr() + self.getResult(ctx.getChild(i))
        # }
        res += self.getResult(ctx.getChild(ctx.getChildCount() - 1))
        return res

    # address를 제외한 모든 변수에 소유자 번호를 붙여줌.
    def visitTypeName(self, ctx: SolidityParser.TypeNameContext):
        # typeName : elementaryTypeName | userDefinedTypeName | mapping;
        vartype = self.getResult(ctx)
        if vartype.strip() != 'address':
            vartype = vartype.rstrip() + self.insertVariableNum()
        return vartype

    # mapping 내에 있는 address에 소유자 번호를 붙여줌.
    def visitElementaryTypeName(self, ctx: SolidityParser.ElementaryTypeNameContext):
        res = self.getResult(ctx)
        if res.strip() == 'address' and self.isParentExist(ctx, SolidityParser.MappingContext):
            res = res.rstrip() + self.insertVariableNum(isAddress=True)
        return res

    # parameter에 소유권자가 표시되어 있으면 위임 표시자를 추가해줌.
    def visitAnnotatedTypeName(self, ctx: SolidityParser.AnnotatedTypeNameContext):
        res = self.visitTypeName(ctx.typeName())
        if self.isParentExist(ctx, SolidityParser.ParameterContext) and '@' in res:
            res = res.rstrip() + '>' + self.insertVariableNum()
        return res

    # AssignmentExpr에서 우항에 _reveal을 넣어줌
    def visitAssignmentExpr(self, ctx: SolidityParser.AssignmentExprContext):
        if self.isParentExist(ctx, SolidityParser.ConstructorDefinitionContext):
            return self.getResult(ctx)
        lhs = self.getResult(ctx.expression(0))
        op = ctx.op.text
        rhs = self.getResult(ctx.expression(1))
        return lhs.rstrip() + ' ' + op + ' ' + '_reveal(' + rhs + ', ' + self.insertVariableNum() + ')'

    # 삼항 연산자를 _reveal로 감싸줌.
    # | cond=expression '?' then_expr=expression ':' else_expr=expression # IteExpr
    def visitIteExpr(self, ctx: SolidityParser.IteExprContext):
        res = self.getResult(ctx)
        return '_reveal(' + res + ', ' + self.insertVariableNum() + ')'

    # Eq expression에 me가 있다면 그냥 돌려주고 me가 없다면 _reveal로 감싸줌.
    def visitEqExpr(self, ctx: SolidityParser.EqExprContext):
        res = self.getResult(ctx)
        for child in ctx.expression():
            tmp = self.getResult(child)
            if tmp.rstrip() == 'me':
                return res
        return '_reveal(' + res + ', ' + self.insertVariableNum() + ')'


class DystonizerStep3(DystonizerStep1_2):

    def __init__(self):
        super(DystonizerStep3, self).__init__()
        self.fOwner = {1: "hospital", 2: "hospital", 3: "c3"}
        self.vStack = OrderedDict()
        self.ESP = []
        self.relation = {}

    def insertFunctionNum(self):
        self.function_num += 1
        return '\n' + self.getTapStr() + '@' + str(self.fOwner[self.function_num]) + '\n'

    def vStackInit(self):
        self.ESP.append(0)

    def vStackPush(self, _idf: str, _type: str):
        self.ESP[-1] += 1
        V = self.stackElemGenerator(_idf, _type) if '@' in _type else Variable(_idf, )
        self.vStack[_idf.rstrip()] = V
        self.relation[V.getOwner()] = V

    def vStackClear(self, originalStr: str = ''):
        if originalStr:
            owners = re.findall('_t\\d*', originalStr)
            for owner in owners:
                if owner in self.relation.keys():
                    originalStr = re.sub(owner, self.relation[owner].getOwner(), originalStr)

            remainedOwners = sorted(list(set(re.findall('_t\\d*', originalStr))))

            contraints = {}
            for idf in self.vStack.keys():
                if self.vStack[idf].getOwner() in remainedOwners:
                    contraints[self.vStack[idf].getOwner()] = self.vStack[idf].getConstraint()
                    if self.vStack[idf].getDel():
                        contraints[self.vStack[idf].getDel()] = [self.vStack['me/all'].getOwner()]

            constraintStr = ''
            constraintStr += ' @@ { { ' + ', '.join(remainedOwners) + ' }\n' if remainedOwners else ' @@ {\n'
            constraintStr += self.TAP * (self.tap_cnt + 1) + f'me == {self.fOwner[self.function_num]}\n'
            for owner in sorted(contraints.keys()):
                constraintStr += self.TAP * (self.tap_cnt + 1)
                constraintStr += f'{owner} == ' + '/'.join(contraints[owner]) + '\n'
            constraintStr = constraintStr.replace('_', '')

            originalStr = originalStr[:-1] + constraintStr + self.getTapStr() + '}\n'

        while self.ESP[-1]:
            self.vStack.popitem(last=True)
            self.ESP[-1] -= 1
        self.ESP.pop()

        return originalStr

    # type@_t1>@_t2 => type, _t1, _t2
    def getAnnotatedType_Type_Owner(self, ats: str):
        ats = ats.replace(' ', '')
        _delegation = ''
        if '>@' in ats:
            _delegation = ats[ats.rfind('>') + 2:]
            ats = ats[:ats.rfind('>')]
        _type, _value = ats[:ats.rfind('@')], ats[ats.rfind('@') + 1:]
        return _type, _value, _delegation

    # mapping(address!_t2=>bool@_t3) -> address, _t2, bool, _t3
    def getMappingType_Key_Value(self, mappingTypeStr: str):
        mappingTypeStr = mappingTypeStr.replace(' ', '')
        key_value = mappingTypeStr[mappingTypeStr.find('(') + 1:-1]
        key, value = key_value.split('=>')
        _key_type, _key_owner = key.split('!')
        _value_type, _value_owner = value.split('@')
        return _key_type, _key_owner, _value_type, _value_owner

    # stack에 Variable 객체를 쌓아줌.
    def stackElemGenerator(self, _idf: str, _raw_type: str):
        _type, _owner, _delegation = self.getAnnotatedType_Type_Owner(_raw_type)
        result = Variable()
        if 'mapping' in _type:
            result.setKeyValue(*self.getMappingType_Key_Value(_type))
            _type = 'mapping'
        result.setIdentifier(_idf)
        if _type:
            result.setType(_type)
        if _delegation:
            result.setOwner(_delegation)
            result.setDel(_owner)
        else:
            result.setOwner(_owner)
        return result

    # expr안에 있는 모든 _reveal의 소유자와 idf를 돌려줌.
    def unpackReveal(self, revealExpr: str):
        idf_owner_dict = {}
        start = revealExpr.find('_reveal(') + 8
        middle = revealExpr.rfind(',')
        end = revealExpr.find(')', middle)
        revealExpr = revealExpr[start:end]
        i = revealExpr.rfind(',')
        _expr, _revealOwner = revealExpr[:i], revealExpr[i + 1:]
        # 안쪽에 나타난 reveal에서 변수들과 reveal 대상 소유자를 추가해줌.
        if '_reveal' in _expr:
            _idf_owner_dict = self.unpackReveal(_expr)
            idf_owner_dict.update(_idf_owner_dict)
        # expr에서 현재 함수내에서 쓰이는 idf를 찾아서 넘겨줌
        idfs = _expr.replace(' ','').split('==') if '==' in _expr else _expr.split()
        for idf in idfs:
            if idf in self.vStack.keys():
                idf_owner_dict[idf] = _revealOwner.strip()[1:]
        return idf_owner_dict

    # contractdefinition을 할 때 ESP를 push convert가 끝나면 stack clear, ESP를 pop한다.
    def visitContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        self.vStackInit()
        self.vStackPush('me/all', '@me/all')
        res = super().visitContractDefinition(ctx)
        self.vStackClear()
        return res

    def visitConstructorDefinition(self, ctx: SolidityParser.ConstructorDefinitionContext):
        self.vStackInit()
        res = super().visitConstructorDefinition(ctx)
        res = self.vStackClear(res)
        return res

    # Function에 들어갈 때 ESP를 push
    # Function이 끝날 때 stack clear, ESP를 pop
    def visitFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        self.vStackInit()
        res = super().visitFunctionDefinition(ctx)
        res = self.vStackClear(res)
        return res

    # stateVariableDeclaration : (keywords+=FinalKeyword)* annotated_type=annotatedTypeName (keywords+=ConstantKeyword)* idf=identifier('=' expr=expression)? ';';
    # 전역 변수를 스택에 저장함.
    def visitStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        res = ''
        for child in ctx.children:
            # annotated_type 실행의 반복을 막으면서 문자열을 생성함.
            if isinstance(child, SolidityParser.AnnotatedTypeNameContext):
                at = self.visitAnnotatedTypeName(ctx.annotatedTypeName())
                if at.rstrip() != 'address':
                    idf = self.visitIdentifier(ctx.identifier())
                    self.vStackPush(idf.rstrip(), at)
                res += at
            else:
                res += self.getResult(child)
        return res

    # parameter : (keywords+=FinalKeyword)? annotated_type=annotatedTypeName idf=identifier? ;
    def visitParameter(self, ctx: SolidityParser.ParameterContext):
        final = self.visitTerminal(ctx.FinalKeyword()) if ctx.FinalKeyword() else ''
        at = self.visitAnnotatedTypeName(ctx.annotatedTypeName())
        idf = self.visitIdentifier(ctx.identifier())
        if at.rstrip() != 'address':
            self.vStackPush(idf.rstrip(), at)
            self.vStack[idf.rstrip()].appendConstraint(self.vStack['me/all'])
        return final + at + idf

    def visitStatement(self, ctx: SolidityParser.StatementContext):
        res = self.getResult(ctx)
        tmpRes = res.strip()
        if isinstance(ctx.getChild(0).getChild(0).getChild(0), SolidityParser.FunctionCallExprContext):
            if '_reveal' in tmpRes:
                expr_reveal_owner_relationship = self.unpackReveal(tmpRes[tmpRes.find('_reveal'):-2])
                for idf, owner in expr_reveal_owner_relationship.items():
                    # 1. owner간의 변환 관계를 저장함.
                    self.relation[owner] = self.vStack[idf]
                    # 2. 소유자 관계를 재설정함.
                    self.vStack[idf].setOwner('_all')
        elif isinstance(ctx.getChild(0).getChild(0).getChild(0), SolidityParser.AssignmentExprContext) and \
                self.isParentExist(ctx, SolidityParser.FunctionDefinitionContext):
            lhs, rhs = tmpRes.split('=')
            expr_reveal_owner_relationship = self.unpackReveal(rhs)
            # 1. owner간의 변환 관계를 저장함.
            for idf, owner in expr_reveal_owner_relationship.items():
                self.relation[owner] = self.vStack[idf]
            # 2. lhs가 mapping 변수라면 rhs와 lhs에 나타난 변수들의 owner를 재설정함
            if '[' in lhs:
                lhs = lhs.replace(' ', '')
                mappingVariable = self.vStack[lhs[:lhs.find('[')]].key_value
                keyOwner, valueOwner = mappingVariable.getKeyOwner(), mappingVariable.getValueOwner()
                lhs = lhs[lhs.find('[') + 1:lhs.find(']')]
                for idf, owner in expr_reveal_owner_relationship.items():
                    self.vStack[idf].setOwner(valueOwner)
                    self.vStackPush(lhs, 'address@' + keyOwner)
            # 3. V간 constraint를 저장함.
            for idf in expr_reveal_owner_relationship.keys():
                if idf != lhs.rstrip():
                    self.vStack[idf].appendConstraint(self.vStack[lhs.rstrip()])
                    self.vStack[lhs.rstrip()].appendConstraint(self.vStack[idf])

        return self.getTapStr() + res
