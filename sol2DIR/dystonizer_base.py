from SolidityParser import SolidityParser
from gen.SolidityVisitor import SolidityVisitor
from antlr4 import *
from collections import defaultdict, deque
from sol2DIR.Variable import Variable
import re


class DystonizerBase(SolidityVisitor):

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

    def visitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        res = self.removeRedundantSpace(self.getResult(ctx).replace('<EOF>', ''))
        print(res)
        return res

    def visitPragmaDirective(self, ctx: SolidityParser.PragmaDirectiveContext):
        return self.getResult(ctx) + '\n'

    def visitVersionPragma(self, ctx: SolidityParser.VersionPragmaContext):
        return self.getResult(ctx)

    def visitVersion(self, ctx: SolidityParser.VersionContext):
        return self.getResult(ctx)

    def visitVersionOperator(self, ctx: SolidityParser.VersionOperatorContext):
        return self.getResult(ctx)

    def visitVersionConstraint(self, ctx: SolidityParser.VersionConstraintContext):
        return self.getResult(ctx)

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

    def visitContractPart(self, ctx: SolidityParser.ContractPartContext):
        return self.getResult(ctx)

    def visitStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        return self.getResult(ctx)

    def visitConstructorDefinition(self, ctx: SolidityParser.ConstructorDefinitionContext):
        return self.getResult(ctx)

    def visitFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        return self.getResult(ctx)

    def visitReturnParameters(self, ctx: SolidityParser.ReturnParametersContext):
        return self.getResult(ctx)

    def visitModifierList(self, ctx: SolidityParser.ModifierListContext):
        return self.getResult(ctx)

    def visitModifier(self, ctx: SolidityParser.ModifierContext):
        return self.getResult(ctx)

    def visitParameterList(self, ctx: SolidityParser.ParameterListContext):
        return self.getResult(ctx)

    def visitParameter(self, ctx: SolidityParser.ParameterContext):
        return self.getResult(ctx)

    def visitEnumValue(self, ctx: SolidityParser.EnumValueContext):
        res = ''
        if ctx.children:
            for child in ctx.children:
                res += self.getTapStr() + self.getResult(child)
        return res

    def visitEnumDefinition(self, ctx: SolidityParser.EnumDefinitionContext):
        return self.getResult(ctx)

    def visitVariableDeclaration(self, ctx: SolidityParser.VariableDeclarationContext):
        return self.getResult(ctx)

    def visitTypeName(self, ctx: SolidityParser.TypeNameContext):
        return self.getResult(ctx)

    def visitUserDefinedTypeName(self, ctx: SolidityParser.UserDefinedTypeNameContext):
        return self.getResult(ctx)

    def visitMapping(self, ctx: SolidityParser.MappingContext):
        return self.getResult(ctx)

    def visitStateMutability(self, ctx: SolidityParser.StateMutabilityContext):
        return self.getResult(ctx)

    def visitBlock(self, ctx: SolidityParser.BlockContext):
        return self.getResult(ctx)

    def visitStatement(self, ctx: SolidityParser.StatementContext):
        res = ''
        if ctx.children:
            for child in ctx.children:
                res += self.getTapStr() + self.getResult(child)
        return res

    def visitExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        return self.getResult(ctx)

    def visitIfStatement(self, ctx: SolidityParser.IfStatementContext):
        return self.getResult(ctx)

    def visitWhileStatement(self, ctx: SolidityParser.WhileStatementContext):
        return self.getResult(ctx)

    def visitSimpleStatement(self, ctx: SolidityParser.SimpleStatementContext):
        return self.getResult(ctx)

    def visitForStatement(self, ctx: SolidityParser.ForStatementContext):
        return self.getResult(ctx)

    def visitDoWhileStatement(self, ctx: SolidityParser.DoWhileStatementContext):
        return self.getResult(ctx)

    def visitContinueStatement(self, ctx: SolidityParser.ContinueStatementContext):
        return self.getResult(ctx)

    def visitBreakStatement(self, ctx: SolidityParser.BreakStatementContext):
        return self.getResult(ctx)

    def visitReturnStatement(self, ctx: SolidityParser.ReturnStatementContext):
        return self.getResult(ctx)

    def visitVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        return self.getResult(ctx)

    def visitElementaryTypeName(self, ctx: SolidityParser.ElementaryTypeNameContext):
        return self.getResult(ctx)

    def visitAndExpr(self, ctx: SolidityParser.AndExprContext):
        return self.getResult(ctx)

    def visitParenthesisExpr(self, ctx: SolidityParser.ParenthesisExprContext):
        return self.getResult(ctx)

    def visitBitwiseOrExpr(self, ctx: SolidityParser.BitwiseOrExprContext):
        return self.getResult(ctx)

    def visitAllExpr(self, ctx: SolidityParser.AllExprContext):
        return self.getResult(ctx)

    def visitIteExpr(self, ctx: SolidityParser.IteExprContext):
        return self.getResult(ctx)

    def visitPowExpr(self, ctx: SolidityParser.PowExprContext):
        return self.getResult(ctx)

    def visitStringLiteralExpr(self, ctx: SolidityParser.StringLiteralExprContext):
        return self.getResult(ctx)

    def visitPlusMinusExpr(self, ctx: SolidityParser.PlusMinusExprContext):
        return self.getResult(ctx)

    def visitCompExpr(self, ctx: SolidityParser.CompExprContext):
        return self.getResult(ctx)

    def visitIndexExpr(self, ctx: SolidityParser.IndexExprContext):
        return self.getResult(ctx)

    def visitSignExpr(self, ctx: SolidityParser.SignExprContext):
        return self.getResult(ctx)

    def visitNumberLiteralExpr(self, ctx: SolidityParser.NumberLiteralExprContext):
        return self.getResult(ctx)

    def visitBitwiseNotExpr(self, ctx: SolidityParser.BitwiseNotExprContext):
        return self.getResult(ctx)

    def visitIdentifierExpr(self, ctx: SolidityParser.IdentifierExprContext):
        return self.getResult(ctx)

    def visitBooleanLiteralExpr(self, ctx: SolidityParser.BooleanLiteralExprContext):
        return self.getResult(ctx)

    def visitMeExpr(self, ctx: SolidityParser.MeExprContext):
        return self.getResult(ctx)

    def visitNotExpr(self, ctx: SolidityParser.NotExprContext):
        return self.getResult(ctx)

    def visitBitShiftExpr(self, ctx: SolidityParser.BitShiftExprContext):
        return self.getResult(ctx)

    def visitBitwiseAndExpr(self, ctx: SolidityParser.BitwiseAndExprContext):
        return self.getResult(ctx)

    def visitMultDivModExpr(self, ctx: SolidityParser.MultDivModExprContext):
        return self.getResult(ctx)

    def visitAssignmentExpr(self, ctx: SolidityParser.AssignmentExprContext):
        return self.getResult(ctx)

    def visitTupleExpr(self, ctx: SolidityParser.TupleExprContext):
        return self.getResult(ctx)

    def visitOrExpr(self, ctx: SolidityParser.OrExprContext):
        return self.getResult(ctx)

    def visitFunctionCallExpr(self, ctx: SolidityParser.FunctionCallExprContext):
        return self.getResult(ctx)

    def visitEqExpr(self, ctx: SolidityParser.EqExprContext):
        return self.getResult(ctx)

    def visitPostCrementExpr(self, ctx: SolidityParser.PostCrementExprContext):
        return self.getResult(ctx)

    def visitPrimitiveCastExpr(self, ctx: SolidityParser.PrimitiveCastExprContext):
        return self.getResult(ctx)

    def visitBitwiseXorExpr(self, ctx: SolidityParser.BitwiseXorExprContext):
        return self.getResult(ctx)

    def visitMemberAccessExpr(self, ctx: SolidityParser.MemberAccessExprContext):
        return self.getResult(ctx)

    def visitPreCrementExpr(self, ctx: SolidityParser.PreCrementExprContext):
        return self.getResult(ctx)

    def visitFunctionCallArguments(self, ctx: SolidityParser.FunctionCallArgumentsContext):
        return self.getResult(ctx)

    def visitTupleExpression(self, ctx: SolidityParser.TupleExpressionContext):
        return self.getResult(ctx)

    def visitElementaryTypeNameExpression(self, ctx: SolidityParser.ElementaryTypeNameExpressionContext):
        return self.getResult(ctx)

    def visitNumberLiteral(self, ctx: SolidityParser.NumberLiteralContext):
        return self.getResult(ctx)

    def visitAnnotatedTypeName(self, ctx: SolidityParser.AnnotatedTypeNameContext):
        return self.getResult(ctx)

    def visitIdentifier(self, ctx: SolidityParser.IdentifierContext):
        return self.getResult(ctx)


class DystonizerStep1_2(DystonizerBase):

    def __init__(self):
        super(DystonizerStep1_2, self).__init__()
        self.variable_num = 1
        self.function_num = 0
        self.vStack = deque()
        self.ESP = []

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

    def vStackInit(self):
        self.ESP.append(0)

    def vStackPush(self, _idf, _type, _owner, _delegation=None):
        self.ESP[-1] += 1
        self.vStack.append(Variable(_idf, _type, _owner, _delegation))

    def vStackPop(self):
        while self.ESP[-1]:
            self.vStack.pop()
            self.ESP[-1] -= 1
        self.ESP.pop()

    def visitContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        # contractDefinition : ('contract') idf=identifier '{' parts+=contractPart* '}';
        res = ''
        # contract identifier {
        for i in range(3):
            res += self.getResult(ctx.getChild(i))
        # ESP에 count를 추가함.
        self.vStackInit()
        # contractParts
        for i in range(3, ctx.getChildCount() - 1):
            # 만약 해당 노드의 자식 타입이 ConstructorDefinitionContext or FunctionDefinitionContext 이면 앞에 prefix를 덧붙임.
            if isinstance(ctx.getChild(i).getChild(0), SolidityParser.ConstructorDefinitionContext) or \
                    isinstance(ctx.getChild(i).getChild(0), SolidityParser.FunctionDefinitionContext):
                res += self.insertFunctionNum()
            res += self.getTapStr() + self.getResult(ctx.getChild(i))
        # }
        res += self.getResult(ctx.getChild(ctx.getChildCount() - 1))
        # stack을 clear해줌.
        self.vStackPop()
        return res

    # 변수 관계만 저장
    def visitParameterList(self, ctx: SolidityParser.ParameterListContext):
        # parameterList : '(' (params+=parameter (',' params+=parameter) * )? ')';
        self.vStackInit()
        res = self.getResult(ctx)
        self.vStackPop()
        return res

    # 변수 관계만 저장
    def visitStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        # stateVariableDeclaration : (keywords+=FinalKeyword)* annotated_type=annotatedTypeName (keywords+=ConstantKeyword)* idf=identifier('=' expr=expression)? ';';
        at = self.visitAnnotatedTypeName(ctx.annotatedTypeName()).rstrip()
        if at != 'address':
            left, right = at.split('>') if at.find('=>') == -1 and at.find('>') != -1 else (at, None)
            _owner = left[left.rfind('@') + 2:]
            _delegation = right[2:] if right else _owner
            _type = 'mapping' if 'mapping' in at else at[:at.find('@')]
            _idf = self.visitIdentifier(ctx.identifier()).rstrip()
            self.vStackPush(_idf, _type, _owner, _delegation)
        # annotated_type의 중복 호출을 막기 위해 child가 annotated_type이면 at를 res에 더해주고 아니면 그냥 돌면서 더해줌.
        res = ''
        for child in ctx.children:
            res += at + ' ' if isinstance(child, SolidityParser.AnnotatedTypeNameContext) else self.getResult(child)
        return res

    # def visitMapping(self, ctx: SolidityParser.MappingContext):
    # mapping : 'mapping' '(' key_type=elementaryTypeName ('!'key_label=identifier)? '=>' value_type=annotatedTypeName ')' ;

    # 변수 관계만 저장
    def visitParameter(self, ctx: SolidityParser.ParameterContext):
        # parameter : (keywords+= FinalKeyword)? annotated_type=annotatedTypeName idf=identifier?;
        at = self.visitAnnotatedTypeName(ctx.annotatedTypeName()).rstrip()
        if at != 'address':
            left, right = at.split('>') if at.find('>') != -1 else (at, None)
            _owner = left[left.rfind('@') + 2:]
            _delegation = right[2:] if right else _owner
            _type = 'mapping' if 'mapping' in at else at[:at.find('@')]
            _idf = self.visitIdentifier(ctx.identifier()).rstrip()
            self.vStackPush(_idf, _type, _owner, _delegation)
        # annotated_type의 중복 호출을 막기 위해 child가 annotated_type이면 at를 res에 더해주고 아니면 그냥 돌면서 더해줌.
        res = ''
        for child in ctx.children:
            res += at + ' ' if isinstance(child, SolidityParser.AnnotatedTypeNameContext) else self.getResult(child)
        return res

    # address를 제외한 모든 변수에 소유자 번호를 붙여줌.
    def visitTypeName(self, ctx: SolidityParser.TypeNameContext):
        vartype = super().visitTypeName(ctx)
        if vartype.strip() != 'address':
            vartype = vartype.rstrip() + self.insertVariableNum()
        return vartype

    # mapping 내에 있는 address에 소유자 번호를 붙여줌.
    def visitElementaryTypeName(self, ctx: SolidityParser.ElementaryTypeNameContext):
        res = super().visitElementaryTypeName(ctx)
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

    def insertFunctionNum(self):
        self.function_num += 1
        return '\n' + self.getTapStr() + '@' + str(self.fOwner[self.function_num]) + '\n'

    # def insertVariableNum(self, isAddress=False):
    #     self.variable_num += 1
    #     prefix = '!_t' if isAddress else '@_t'
    #     return prefix + str(self.vOwner[self.variable_num]) + ' '

    def visitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        return super().visitSourceUnit(ctx)
